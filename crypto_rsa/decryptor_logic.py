from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os
import os.path
import binascii
import sys


# 读取 非对称加密 的 私钥
with open(os.path.join(os.path.dirname(sys.argv[0]), "private_key.pem"), "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )


def decryptor(tmp_dir):
    # 读取 对称加密 的 初始化向量iv
    with open(os.path.join(tmp_dir, "aesiv.hex"), "rb") as iv_buffer:
        iv = iv_buffer.read()
        # print("iv", iv)
        # 读取 经过 非对称加密 处理 后的 对称加密的秘钥key
        with open(os.path.join(tmp_dir, "aeskey.hex.enc"), "rb") as encrypted_key_buffer:
            encrypted_key = encrypted_key_buffer.read()
            # 利用 非对称加密的私钥 解密 经过非对称加密处理 的 对称加密的秘钥key
            plain_key_hex = private_key.decrypt(
                encrypted_key,
                padding.PKCS1v15()
            )
            # print("plain_key_hex", plain_key_hex)  # b'26C60B2B480E968E7655705C28C10F5F523FBCA9415C784FC40DB7E68009962F'   -   十六进制值表示的的bytes

    # 读取 经过 对称加密处理后的 fibx2 enc 文件。 ps: 这里的enc 意为 encrypt
    with open(os.path.join(tmp_dir, "data.enc"), "rb") as fibx_enc_buffer:
        fibx_enc = fibx_enc_buffer.read()

    plain_key_unhex = binascii.unhexlify(plain_key_hex)
    # print("plain_key_unhex", plain_key_unhex)  # b'&\xc6\x0b+H\x0e\x96\x8evUp\\(\xc1\x0f_R?\xbc\xa9A\\xO\xc4\r\xb7\xe6\x80\t\x96/'   -   \x形式表示的bytes


    iv = binascii.unhexlify(iv)
    # print("iv", iv)

    cipher = Cipher(algorithms.AES(plain_key_unhex), modes.CBC(iv), backend=default_backend())

    decryptor = cipher.decryptor()

    decrypted_text = decryptor.update(fibx_enc) + decryptor.finalize()

    with open(os.path.join(tmp_dir, "data"), "wb") as fibx_buffer:
        fibx_buffer.write(decrypted_text)
