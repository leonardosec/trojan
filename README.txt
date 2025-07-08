Olá, aqui irei explicar como criei meu primeiro trojan básico com server local.
Aqui também irei passar o código e para o que cada um serve.
Recomendo primeiro escrever os códigos e pra depois ir usando de 1 por 1.

Kerneltroia

O trojan foi feito para testes locais, eu testei ele no Windows defender e no AVG, e ele foi detectado somente pelo AVG ou seja, ele passou pelo Windows defender. Vamos direto para o assunto.
---------------------------------------------------------------------------------------------------------------------------------------------------------
1 - pip install pycryptodome pyinstaller pynput pyautogui

Você irá precisar dessas bibliotecas, especialmente da pyinstaller, ele é quem vai gerar seu .exe


2 - Sever.py
O primeiro script a ser usado vai ser ele, ele vai fazer a sua maquina escutar tudo o que se conectar nela. quando o seu .exe estiver pronto ligue o server.py e aguarde a conexão.

3 - payload.py
Aqui é onde a gente começa a moldar o trojan, esse script ele inclui: 

- Shell reversa interativa
- Keylogger com log em memória
- Captura de tela
- Exfiltração de arquivos `.txt`, `.docx`, `.pdf`, `.jpg`

Depois vamos precisar criptografar ele para gerar o .exe

O próximo passo vai ser criar um encriptador para criptogradar o payload.py, ele vai ser criptografado com AES-256, isso converte o código malicioso em um arquivo criptografado (payload.enc) que o Defender não consegue analisar até ser descriptografado em tempo real pelo loader.

4 - encryptor.py 
No terminal execute: python3 encryptor.py
Isso vai gerar o arquivo `payload.enc`, criptografado com AES-256 usando `senhaforte123` como chave, você vai precisar dessa chave depois.

5 - loader_embedded.py
Na linha que contém o “__REPLACE_ME__” você vai substituir pelo que foi gerado no “payload.enc”.
coloque toda o payload dentro das aspas por exemplo:
> PAYLOAD_ENCRYPTED = b"""TIXkRJHwFvtVTd8ZrpUtQMl81KX136…”""

6 - embedder.py
No terminal execute: python embedder.py
Depois que o codigo estiver pronto iremos precisar desse penultimo, ele vai gerar o payload final para depois gerar o .exe.

7 - final_loader.py
Ele vai gerar o fina_loadder.py, ele vai gerar o um código simples pra você, o que eu to publicando aqui já tem varias outras funções, e tentativa persistência também, dê uma lida no código para entender.

8 - .EXE

Agora vamos para a geração do .exe

faça a instalação dessas bibliotecas:
> pip install pycryptodome pyinstaller pynput pyautogui
A principal a ser instalada é o pyinstaller

Antes tem uma coisa importante a ser comentada, gera o seu .exe em um Windows, se você criar em qualquer ambiente Linux ele não vai gerar o .exe e sim um arquivo para Linux, e ele não vai ser executado da forma certa.

Abras o powershell na pasta em que está o seu final_loader.py e passe esse comando aqui:

> pyinstaller --noconsole --onefile --hidden-import=pynput --hidden-import=pyautogui final_loade.py

Ele vai começar a gerar, depois que terminar ele vai gerar 2 pastas, vá até a "dist" e la está o seu .exe
Depois é só testar ele em um ambiente controlado.

Se você quiser testar no seu Windows, recomendo desativar o antivírus e deixar só Windows defender, se o seu antivírus pegar ele podar acabar excluindo ele.

Novamente dizendo é só para fins educacionais, não me responsabilizo por nada.