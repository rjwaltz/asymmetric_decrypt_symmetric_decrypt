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



# 加载已有的私钥字符串文本
# 这里假设私钥字符串文本存在 private_key.pem 中
with open(os.path.join(os.path.dirname(__file__), "private_key.pem"), "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# 明文
plaintext = b"Hello, world!"

# 对称加密算法AES256
# 生成随机的 初始化向量iv
iv = os.urandom(16)
# 使用PBKDF2进行密钥派生
password = b"some_secure_password"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
# 得到 对称加密 的 symmetric_key
symmetric_key = kdf.derive(password)

# 对称加密: 使用 对称加密的秘钥symmetric_key + 初始化向量iv 来加密明文
cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()
# 得到 经过 对称加密 处理后 的密文
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# 使用 非对称加密的公钥 加密 对称加密的秘钥symmetric_key
encrypted_symmetric_key = private_key.public_key().encrypt(
    symmetric_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)


# ---分割线---
# 已知: 1. 非对称加密的私钥（即private_key）  2. 由非对称加密处理后的对称加密的秘钥（即encrypted_symmetric_key）  3. 初始化向量iv  4. 由对称加密处理后的密文（即ciphertext）
# 如何利用 1、2、3、4 获得 对称加密处理前的明文
# ---分割线---


# 使用 非对称加密的私钥 解密 由非对称加密处理后的对称加密的秘钥symmetric_key
plain_key = private_key.decrypt(
    encrypted_symmetric_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

cipher = Cipher(algorithms.AES(plain_key), modes.CFB(iv), backend=default_backend())

# 解密 由对称加密处理后得到的密文
decryptor = cipher.decryptor()
decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()


print("symmetric_key:", symmetric_key)
print("[encrypted_symmetric_key]:", encrypted_symmetric_key)

print("Ciphertext:", ciphertext)
print("Decrypted text:", decrypted_text)