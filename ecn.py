from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64


def derivate(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # Adjust as necessary
        salt=salt,
        length=32  # Key size in bytes (256 bits)
    )
    return kdf.derive(password.encode())


def encrypt(texto, password):
    salt = b'/-_#'
    clave = derivate(password, salt)
    iv = b'\x00' * 16  # You can generate a random IV for better security
    cipher = Cipher(algorithms.AES(clave), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    texto_encriptado = encryptor.update(texto.encode()) + encryptor.finalize()
    return base64.urlsafe_b64encode(salt + texto_encriptado)


def decrypt(texto_encriptado, password):
    datos = base64.urlsafe_b64decode(texto_encriptado)
    salt = datos[:4]
    texto_encriptado = datos[4:]
    clave = derivate(password, salt)
    iv = b'\x00' * 16  # You can generate a random IV for better security
    cipher = Cipher(algorithms.AES(clave), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    texto_original = decryptor.update(texto_encriptado) + decryptor.finalize()
    return texto_original.decode()

# Ejemplo de uso:
