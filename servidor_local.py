# -*- coding: utf-8 -*-
"""
Servidor Web Local para PRO-ELÉTRICA CAD NBR 5410
Permite abrir a aplicação em qualquer navegador na rede local (Wi-Fi / LAN)
via Celular, Tablet, Notebook ou outro Computador.
"""

import os
import sys
import socket
import http.server
import socketserver
import webbrowser
from urllib.parse import unquote

# Configura codificação do console para UTF-8 de forma segura
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORTA_PADRAO = 8080

def obter_ips_locais():
    ips = []
    try:
        nome_host = socket.gethostname()
        for ip in socket.gethostbyname_ex(nome_host)[2]:
            if not ip.startswith('127.') and not ip.startswith('169.254.'):
                ips.append(ip)
    except Exception:
        pass
    
    if not ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
            s.close()
        except Exception:
            ips.append("127.0.0.1")
    return list(dict.fromkeys(ips))

def desenhar_banner(ip_principal, porta):
    url_local = f"http://localhost:{porta}"
    url_rede = f"http://{ip_principal}:{porta}"

    print("\n" + "=" * 68)
    print("   [+] PRO-ELETRICA CAD NBR 5410 - SERVIDOR WEB ATIVO")
    print("=" * 68)
    print("\n  O software esta pronto para ser aberto em QUALQUER dispositivo!")
    print("\n  >> NO CELULAR OU TABLET (Conectado ao mesmo Wi-Fi):")
    print(f"     URL: {url_rede}")
    print("\n  >> NESTE COMPUTADOR:")
    print(f"     URL: {url_local}")
    print("\n  >> PELA INTERNET (Fora de casa / Clientes):")
    print("     Consulte o botao 'Abrir em Outro Navegador' dentro do sistema")
    print("     para publicar gratuitamente em 10 segundos no Netlify/Vercel.")
    print("\n" + "-" * 68)
    print("  [Pressione CTRL + C para encerrar o servidor]")
    print("=" * 68 + "\n")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_GET(self):
        caminho = unquote(self.path.split('?')[0])
        if caminho in ('/', ''):
            if os.path.exists('index.html'):
                self.path = '/index.html'
            elif os.path.exists('Projeto elétrico.html'):
                self.path = '/Projeto%20el%C3%A9trico.html'
        super().do_GET()

def main():
    diretorio = os.path.dirname(os.path.abspath(__file__))
    os.chdir(diretorio)

    ips = obter_ips_locais()
    ip_principal = ips[0] if ips else "127.0.0.1"

    porta = PORTA_PADRAO
    servidor = None

    for p in range(porta, porta + 10):
        try:
            socketserver.TCPServer.allow_reuse_address = True
            servidor = socketserver.TCPServer(('0.0.0.0', p), CustomHandler)
            porta = p
            break
        except OSError:
            continue

    if not servidor:
        print(f"Erro: Nao foi possivel vincular o servidor as portas {PORTA_PADRAO}-{PORTA_PADRAO+9}")
        sys.exit(1)

    desenhar_banner(ip_principal, porta)

    # Abre automaticamente no navegador padrao deste PC
    try:
        webbrowser.open(f"http://localhost:{porta}")
    except Exception:
        pass

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado com sucesso.")
        servidor.server_close()

if __name__ == '__main__':
    main()
