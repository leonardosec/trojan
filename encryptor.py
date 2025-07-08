# encryptor.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

def pad(data):
    # AES exige múltiplos de 16 bytes
    return data + b' ' * (16 - len(data) % 16)

def encrypt_file(payload_file, output_file, key_str):
    key = hashlib.sha256(key_str.encode()).digest()  # Chave de 32 bytes
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(payload_file, "rb") as f:
        plaintext = pad(f.read())

    ciphertext = cipher.encrypt(plaintext)
    encrypted_data = base64.b64encode(iv + ciphertext)

    with open(output_file, "wb") as f:
        f.write(encrypted_data)

    print(f"[+] Payload criptografado com sucesso para '{output_file}'.")

if __name__ == "__main__":
    # parâmetros
    PAYLOAD_FILE = "payload.py"
    OUTPUT_FILE = "payload.enc"
    ENCRYPTION_KEY = "senhaforte123"  # você pode trocar

    encrypt_file(PAYLOAD_FILE, OUTPUT_FILE, ENCRYPTION_KEY)