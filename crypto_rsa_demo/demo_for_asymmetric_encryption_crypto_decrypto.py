from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import ciphers
import os.path

from pathlib import Path

print(Path(".").resolve())

print(os.path.dirname(__file__))

with open(os.path.join(os.path.dirname(__file__), "private_key.pem"), "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )


with open(os.path.join(os.path.dirname(__file__), "public_key.pem"), "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )


plaintext = b"Hello, world!"
print(plaintext)
cipher_text = public_key.encrypt(
    plaintext,
    asymmetric_padding.OAEP(
        mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)


decrypted_text = private_key.decrypt(
    cipher_text,
    asymmetric_padding.OAEP(
        mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print(decrypted_text.decode('utf-8'))