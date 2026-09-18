# -*- coding: utf-8 -*-
"""
Script to inject PWA features into index.html and sync with Projeto elétrico.html
"""
import re

def apply_pwa():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print("Original size:", len(html))

    # 1. INJECT PWA META TAGS IN <head>
    head_pwa = """    <!-- PWA Manifest & App Configuration -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#0f172a">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="ProElétrica">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <link rel="icon" type="image/svg+xml" href="icon.svg">
    <link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
"""

    if '<link rel="manifest"' not in html:
        target_head = '<title>PRO-ELÉTRICA CAD NBR 5410</title>'
        html = html.replace(target_head, target_head + '\n' + head_pwa, 1)
        print("PWA meta tags injected into <head>.")
    else:
        print("PWA meta tags already present in <head>.")

    # 2. INJECT INSTALL BUTTON INTO MOBILE TOP HEADER
    # We want to add btnInstalarAppMobile before btnMobilePavimentoBadge
    btn_mobile_install = """                <button id="btnInstalarAppMobile" onclick="dispararInstalacaoPWA()" class="bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-slate-950 font-black px-2 py-1 rounded-lg text-[10px] flex items-center gap-1 shadow transition" title="Instalar Aplicativo no Celular">
                    <i class="fa-solid fa-download"></i> Instalar
                </button>
"""
    target_mobile_header = '            <!-- SELETOR RÁPIDO DE PAVIMENTO MOBILE & AÇÕES -->'
    if 'id="btnInstalarAppMobile"' not in html and target_mobile_header in html:
        html = html.replace(target_mobile_header, target_mobile_header + '\n' + btn_mobile_install, 1)
        print("Mobile Install Button injected into mobile top header.")

    # 3. INJECT PWA BANNER INTO MOBILE DRAWER MENU
    drawer_banner = """                    <!-- PWA BANNER NO DRAWER -->
                    <div id="pwaBannerDrawer" class="bg-gradient-to-r from-amber-500/15 via-sky-500/15 to-purple-500/15 border border-amber-500/30 p-3 rounded-xl space-y-2">
                        <div class="flex items-center gap-2">
                            <span class="w-7 h-7 rounded-lg bg-amber-500 text-slate-950 flex items-center justify-center text-xs font-black shadow">
                                <i class="fa-solid fa-mobile-screen-button"></i>
                            </span>
                            <div>
                                <h4 class="font-bold text-white text-xs">Instalar Aplicativo</h4>
                                <p class="text-[10px] text-slate-300">Acesse direto da tela inicial em tela cheia</p>
                            </div>
                        </div>
                        <button onclick="dispararInstalacaoPWA(); fecharDrawerMobile();" class="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold py-1.5 px-3 rounded-lg text-xs flex items-center justify-center gap-1.5 transition shadow">
                            <i class="fa-solid fa-download"></i> Adicionar à Tela Inicial
                        </button>
                    </div>
"""
    target_drawer = '                    <!-- GESTÃO DE PROJETOS -->'
    if 'id="pwaBannerDrawer"' not in html and target_drawer in html:
        html = html.replace(target_drawer, drawer_banner + '\n' + target_drawer, 1)
        print("PWA Banner injected into drawer.")

    # 4. INJECT INSTALL BUTTON IN DESKTOP SUBBAR / HEADER
    desktop_install = """                <button id="btnInstalarAppDesktop" onclick="dispararInstalacaoPWA()" class="bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 shadow-sm" title="Instalar como aplicativo no computador">
                    <i class="fa-solid fa-download text-amber-400"></i> <span>Instalar App</span>
                </button>"""
    # Look for button opening project manager or quick save in desktop subbar
    target_desktop = '<button onclick="abrirModalImpressaoPDF()"'
    if 'id="btnInstalarAppDesktop"' not in html and target_desktop in html:
        html = html.replace(target_desktop, desktop_install + '\n                ' + target_desktop, 1)
        print("Desktop Install Button injected.")

    # 5. INJECT IOS INSTRUCTIONS MODAL
    ios_modal = """    <!-- MODAL DE INSTRUÇÕES PWA IOS -->
    <div id="modalInstrucoesIOS" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-slate-900 border border-slate-700 w-full max-w-sm rounded-2xl p-5 shadow-2xl space-y-4 text-center">
            <div class="w-12 h-12 rounded-2xl bg-amber-500/20 text-amber-400 border border-amber-500/40 flex items-center justify-center text-2xl mx-auto shadow-inner">
                <i class="fa-brands fa-apple"></i>
            </div>
            <h3 class="text-base font-bold text-white">Instalar no iPhone / iPad</h3>
            <p class="text-xs text-slate-300 leading-relaxed text-left">
                No navegador Safari do seu dispositivo Apple, siga estes 2 passos:
            </p>
            <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 text-left space-y-2.5 text-xs">
                <div class="flex items-start gap-2.5 text-slate-200">
                    <span class="w-5 h-5 rounded-full bg-slate-800 text-amber-400 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">1</span>
                    <span>Toque no botão <strong>Compartilhar</strong> (<i class="fa-solid fa-arrow-up-from-bracket text-sky-400 mx-1"></i>) localizado na barra inferior do Safari.</span>
                </div>
                <div class="flex items-start gap-2.5 text-slate-200">
                    <span class="w-5 h-5 rounded-full bg-slate-800 text-amber-400 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">2</span>
                    <span>Role para cima e toque em <strong>"Adicionar à Tela de Início"</strong> (<i class="fa-regular fa-square-plus text-emerald-400 mx-1"></i>).</span>
                </div>
            </div>
            <button onclick="document.getElementById('modalInstrucoesIOS').classList.add('hidden')" class="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold py-2.5 rounded-xl text-xs transition shadow">
                OK, Entendi
            </button>
        </div>
    </div>
"""
    if 'id="modalInstrucoesIOS"' not in html:
        # Put right before </body>
        html = html.replace('</body>', ios_modal + '\n</body>', 1)
        print("iOS Instructions modal injected.")

    # 6. INJECT SERVICE WORKER & PWA JAVASCRIPT
    pwa_script = """
    // =========================================================================
    // PWA & SERVICE WORKER LIFECYCLE HANDLERS
    // =========================================================================
    let deferredPromptPWA = null;

    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('./sw.js')
                .then(reg => console.log('[PWA] Service Worker ativo:', reg.scope))
                .catch(err => console.log('[PWA] Erro ao registrar Service Worker:', err));
        });
    }

    window.addEventListener('beforeinstallprompt', (e) => {
        // Previne o infobar automático para que possamos usar nosso botão estilizado
        e.preventDefault();
        deferredPromptPWA = e;
        console.log('[PWA] Evento beforeinstallprompt capturado');
        const btnM = document.getElementById('btnInstalarAppMobile');
        const btnD = document.getElementById('btnInstalarAppDesktop');
        if (btnM) btnM.classList.remove('hidden');
        if (btnD) btnD.classList.remove('hidden');
    });

    window.addEventListener('appinstalled', () => {
        console.log('[PWA] Aplicativo instalado com sucesso!');
        deferredPromptPWA = null;
        const btnM = document.getElementById('btnInstalarAppMobile');
        const btnD = document.getElementById('btnInstalarAppDesktop');
        if (btnM) btnM.classList.add('hidden');
        if (btnD) btnD.classList.add('hidden');
    });

    function dispararInstalacaoPWA() {
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
        if (deferredPromptPWA) {
            deferredPromptPWA.prompt();
            deferredPromptPWA.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('[PWA] Usuário aceitou a instalação');
                } else {
                    console.log('[PWA] Usuário recusou a instalação');
                }
                deferredPromptPWA = null;
            });
        } else if (isIOS) {
            const m = document.getElementById('modalInstrucoesIOS');
            if (m) m.classList.remove('hidden');
        } else {
            // Em navegadores de computador ou quando já instalado
            const m = document.getElementById('modalInstrucoesIOS');
            if (m) {
                m.classList.remove('hidden');
            } else {
                alert('Para instalar o aplicativo no seu dispositivo: No menu do navegador (três pontos ⋮), selecione "Instalar PRO-ELÉTRICA" ou "Adicionar à tela inicial".');
            }
        }
    }
"""

    if 'deferredPromptPWA' not in html:
        target_script_end = '</script>\n</body>'
        if target_script_end in html:
            html = html.replace(target_script_end, pwa_script + '\n</script>\n</body>', 1)
            print("PWA script injected before </script>.")
        else:
            # Fallback
            html = html.replace('</body>', '<script>' + pwa_script + '</script>\n</body>', 1)
            print("PWA script injected in new script tag.")

    # Save index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html saved, new size:", len(html))

    # Sync to Projeto elétrico.html
    with open('Projeto elétrico.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Projeto elétrico.html synchronized.")

if __name__ == '__main__':
    apply_pwa()
