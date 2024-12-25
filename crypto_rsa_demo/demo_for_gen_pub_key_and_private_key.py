from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os.path

# 生成RSA密钥对
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# 序列化私钥
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# 生成对应的公钥
public_key = private_key.public_key()
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 将密钥对保存到文件
with open(os.path.join(os.path.dirname(__file__), 'private_key.pem'), 'wb') as f:
    f.write(private_key_pem)
    
with open(os.path.join(os.path.dirname(__file__), 'public_key.pem'), 'wb') as f:
    f.write(public_key_pem)