# -*- coding: utf-8 -*-
"""
Script to apply Mobile & Tablet Optimization to index.html and sync to Projeto elétrico.html
"""
import re

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print("Initial length:", len(html))

    # =========================================================================
    # 1. CSS UPDATES FOR MOBILE & TABLET (TOUCH, SAFE-AREA, BOTTOM NAV, DRAWER)
    # =========================================================================
    old_style_end = """        .din-rail-bg {
            background: linear-gradient(180deg, #1e293b 0%, #334155 35%, #475569 50%, #334155 65%, #1e293b 100%);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);
        }
    </style>"""

    new_style_end = """        .din-rail-bg {
            background: linear-gradient(180deg, #1e293b 0%, #334155 35%, #475569 50%, #334155 65%, #1e293b 100%);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.6);
        }

        /* OTIMIZAÇÕES MOBILE & TABLET (TOUCH & RESPONSIVIDADE) */
        @media (max-width: 1023px) {
            body {
                overflow-x: hidden;
                -webkit-tap-highlight-color: transparent;
            }
            .mobile-bottom-nav {
                display: flex !important;
            }
            .desktop-only-header {
                display: none !important;
            }
            .desktop-only-subbar {
                display: none !important;
            }
            .desktop-only-tabs {
                display: none !important;
            }
            .mobile-top-header {
                display: flex !important;
            }
            .canvas-container-responsive {
                height: 400px !important;
            }
            canvas {
                touch-action: none;
            }
        }
        @media (min-width: 1024px) {
            .mobile-bottom-nav {
                display: none !important;
            }
            .mobile-top-header {
                display: none !important;
            }
            .mobile-fab {
                display: none !important;
            }
        }

        /* Botão Flutuante (FAB) Mobile */
        .mobile-fab-btn {
            box-shadow: 0 8px 24px -2px rgba(245, 158, 11, 0.45);
        }
        /* Drawer Sheet */
        .mobile-drawer-sheet {
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
    </style>"""

    if old_style_end in html:
        html = html.replace(old_style_end, new_style_end, 1)
        print("CSS Mobile Styles injected.")
    else:
        print("WARNING: old_style_end not found!")

    # =========================================================================
    # 2. BODY & CONTAINER: Adjust padding for bottom nav
    # =========================================================================
    old_body_container = '<div class="max-w-7xl mx-auto px-4 py-6">'
    new_body_container = '<div class="max-w-7xl mx-auto px-2.5 sm:px-4 pt-2 pb-24 lg:py-6">'
    if old_body_container in html:
        html = html.replace(old_body_container, new_body_container, 1)
        print("Body container padding adjusted.")
    else:
        print("WARNING: old_body_container not found!")

    # =========================================================================
    # 3. ADD MOBILE TOP HEADER & DRAWER BEFORE DESKTOP HEADER
    # =========================================================================
    old_header_start = '        <!-- CABEÇALHO -->'
    mobile_top_header = """        <!-- MOBILE TOP HEADER (VISÍVEL APENAS EM CELULARES E TABLETS) -->
        <div class="mobile-top-header hidden bg-slate-900/95 backdrop-blur-md border border-slate-800 rounded-2xl p-3 mb-3 shadow-xl flex justify-between items-center no-print sticky top-2 z-30">
            <div class="flex items-center gap-2">
                <span class="w-8 h-8 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/40 flex items-center justify-center text-sm shadow">
                    <i class="fa-solid fa-bolt-lightning"></i>
                </span>
                <div>
                    <h1 class="text-sm font-black tracking-tight text-amber-400 flex items-center gap-1.5 leading-none">
                        PRO-ELÉTRICA
                    </h1>
                    <span class="text-[9px] text-slate-400 font-mono">NBR 5410 • CAD/BIM</span>
                </div>
            </div>

            <!-- SELETOR RÁPIDO DE PAVIMENTO MOBILE & AÇÕES -->
            <div class="flex items-center gap-1.5">
                <button onclick="alternarPavimentoMobile()" id="btnMobilePavimentoBadge" class="bg-sky-500/20 text-sky-300 border border-sky-500/40 px-2.5 py-1 rounded-lg text-[11px] font-bold flex items-center gap-1 shadow-sm">
                    <i class="fa-solid fa-layer-group text-[10px]"></i> <span id="lblNomePavimentoMobile">Térreo</span> ▾
                </button>
                <button onclick="abrirModalImpressaoPDF()" class="bg-blue-600 hover:bg-blue-500 text-white p-1.5 rounded-lg text-xs font-bold transition flex items-center justify-center shadow" title="Imprimir PDF">
                    <i class="fa-solid fa-print"></i>
                </button>
                <button onclick="salvarPontoRapido()" class="bg-amber-600 hover:bg-amber-500 text-white p-1.5 rounded-lg text-xs font-bold transition flex items-center justify-center shadow" title="Salvar Ponto">
                    <i class="fa-solid fa-floppy-disk"></i>
                </button>
                <button onclick="abrirDrawerMobile()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 p-1.5 rounded-lg text-xs font-bold transition flex items-center justify-center shadow" title="Menu Completo">
                    <i class="fa-solid fa-bars"></i>
                </button>
            </div>
        </div>

        <!-- DRAWER / MENU COMPLETO MOBILE (OFFCANVAS) -->
        <div id="drawerMenuMobile" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex justify-end hidden p-0">
            <div class="bg-slate-900 border-l border-slate-800 w-full max-w-xs h-full p-4 overflow-y-auto space-y-4 text-xs shadow-2xl flex flex-col justify-between">
                <div class="space-y-4">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-drafting-compass text-amber-400 text-lg"></i>
                            <h3 class="font-bold text-white text-sm">Ferramentas & Ajustes</h3>
                        </div>
                        <button onclick="fecharDrawerMobile()" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800">
                            <i class="fa-solid fa-xmark text-base"></i>
                        </button>
                    </div>

                    <!-- GESTÃO DE PROJETOS -->
                    <div class="space-y-1.5">
                        <span class="text-[10px] uppercase font-bold text-amber-400 tracking-wider">Projetos & Versões</span>
                        <div class="grid grid-cols-2 gap-1.5">
                            <button onclick="abrirModalNovoProjeto(); fecharDrawerMobile();" class="bg-emerald-700 hover:bg-emerald-600 text-white font-bold p-2 rounded-xl transition flex flex-col items-center gap-1 text-[10px] text-center">
                                <i class="fa-solid fa-folder-plus text-xs"></i> Novo Projeto
                            </button>
                            <button onclick="abrirModalGerenciarProjetos(); fecharDrawerMobile();" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold p-2 rounded-xl transition flex flex-col items-center gap-1 text-[10px] text-center">
                                <i class="fa-solid fa-clock-rotate-left text-amber-400 text-xs"></i> Versões Salvas
                            </button>
                        </div>
                    </div>

                    <!-- PAVIMENTOS E LAJES -->
                    <div class="space-y-1.5">
                        <span class="text-[10px] uppercase font-bold text-sky-400 tracking-wider">Pavimentos & Infraestrutura</span>
                        <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 space-y-2">
                            <div class="flex justify-between items-center">
                                <span class="text-slate-300 font-semibold">Andar:</span>
                                <div id="containerBotoesPavimentosMobile" class="flex gap-1"></div>
                            </div>
                            <div class="flex justify-between items-center pt-1 border-t border-slate-850">
                                <span class="text-slate-400 text-[10px]">Passagem:</span>
                                <div class="flex gap-1">
                                    <button onclick="alterarPassagemCabos('teto')" class="bg-sky-600 text-white text-[10px] px-2 py-1 rounded font-bold">Teto</button>
                                    <button onclick="alterarPassagemCabos('chao')" class="bg-slate-800 text-slate-300 text-[10px] px-2 py-1 rounded font-bold">Chão</button>
                                </div>
                            </div>
                            <button onclick="abrirModalNovoPavimento(); fecharDrawerMobile();" class="w-full bg-slate-800 hover:bg-slate-700 text-sky-300 font-bold p-1.5 rounded-lg border border-slate-700 transition text-[10px] flex items-center justify-center gap-1">
                                <i class="fa-solid fa-plus text-[9px]"></i> Criar Novo Andar
                            </button>
                        </div>
                    </div>

                    <!-- EXPORTAÇÕES E IMPRESSÃO -->
                    <div class="space-y-1.5">
                        <span class="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">Exportações & Relatórios</span>
                        <div class="space-y-1">
                            <button onclick="abrirModalImpressaoPDF(); fecharDrawerMobile();" class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold p-2 rounded-xl transition flex items-center justify-center gap-2 text-xs shadow">
                                <i class="fa-solid fa-file-pdf text-amber-300"></i> Imprimir 6 Pranchas PDF
                            </button>
                            <button onclick="exportarParaExcel(); fecharDrawerMobile();" class="w-full bg-emerald-700 hover:bg-emerald-600 text-white font-bold p-2 rounded-xl transition flex items-center justify-center gap-2 text-xs">
                                <i class="fa-solid fa-file-excel text-sm"></i> Exportar Lista Excel (.xlsx)
                            </button>
                            <button onclick="abrirModalImportar(); fecharDrawerMobile();" class="w-full bg-indigo-700 hover:bg-indigo-600 text-white font-bold p-2 rounded-xl transition flex items-center justify-center gap-2 text-xs">
                                <i class="fa-solid fa-file-import"></i> Importar Planta CAD / DWG
                            </button>
                        </div>
                    </div>
                </div>

                <div class="pt-3 border-t border-slate-800 text-[10px] text-slate-500 text-center">
                    PRO-ELÉTRICA CAD NBR 5410 • Versão Mobile
                </div>
            </div>
        </div>

"""

    # Add class desktop-only-header to the desktop header
    old_desktop_header = '<header class="bg-slate-900 border border-slate-800 text-white rounded-2xl p-6 shadow-2xl mb-6 flex flex-col md:flex-row justify-between items-center no-print">'
    new_desktop_header = '<header class="desktop-only-header bg-slate-900 border border-slate-800 text-white rounded-2xl p-6 shadow-2xl mb-6 flex flex-col md:flex-row justify-between items-center no-print">'

    if old_header_start in html and old_desktop_header in html:
        html = html.replace(old_header_start, mobile_top_header + "        " + old_header_start, 1)
        html = html.replace(old_desktop_header, new_desktop_header, 1)
        print("Mobile top header and drawer added.")
    else:
        print("WARNING: header replacement bounds not found!")

    # Add class desktop-only-subbar to the desktop subbar (lines 98)
    old_desktop_subbar = '<div class="bg-slate-900 p-4 rounded-2xl border border-slate-800 mb-6 flex flex-col xl:flex-row justify-between items-center gap-4 no-print">'
    new_desktop_subbar = '<div class="desktop-only-subbar bg-slate-900 p-4 rounded-2xl border border-slate-800 mb-6 flex flex-col xl:flex-row justify-between items-center gap-4 no-print">'
    if old_desktop_subbar in html:
        html = html.replace(old_desktop_subbar, new_desktop_subbar, 1)
        print("Desktop subbar tagged.")

    # Tag desktop navigation tabs
    old_nav_tabs = '<nav class="flex border-b border-slate-800 mb-6 space-x-2 no-print overflow-x-auto">'
    new_nav_tabs = '<nav class="desktop-only-tabs flex border-b border-slate-800 mb-6 space-x-2 no-print overflow-x-auto">'
    if old_nav_tabs in html:
        html = html.replace(old_nav_tabs, new_nav_tabs, 1)
        print("Desktop nav tabs tagged.")

    # =========================================================================
    # 4. ADD MOBILE FLOATING ACTION BUTTON (FAB) & MOBILE BOTTOM NAVIGATION BAR
    # =========================================================================
    mobile_floating_widgets = """
    <!-- MOBILE FLOATING ACTION BUTTON (FAB: + RÁPIDO PARA ADICIONAR ELEMENTOS) -->
    <div class="mobile-fab fixed bottom-20 right-4 z-40 flex flex-col items-end gap-2 no-print">
        <!-- Speed Dial Items (Ocultos por padrão, alternados ao clicar no FAB) -->
        <div id="mobileSpeedDialItems" class="hidden flex-col items-end gap-2 mb-1">
            <button onclick="abrirModalPontoNovo('TUG'); toggleSpeedDialMobile();" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-1.5 px-3 rounded-xl shadow-lg flex items-center gap-2 text-xs border border-emerald-400/40">
                <span>+ Tomada TUG</span> <i class="fa-solid fa-plug text-xs"></i>
            </button>
            <button onclick="abrirModalPontoNovo('TUE'); toggleSpeedDialMobile();" class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-1.5 px-3 rounded-xl shadow-lg flex items-center gap-2 text-xs border border-blue-400/40">
                <span>+ Tomada TUE</span> <i class="fa-solid fa-bolt text-xs"></i>
            </button>
            <button onclick="abrirModalPontoNovo('ILUM'); toggleSpeedDialMobile();" class="bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold py-1.5 px-3 rounded-xl shadow-lg flex items-center gap-2 text-xs border border-amber-300">
                <span>+ Lâmpada</span> <i class="fa-solid fa-lightbulb text-xs"></i>
            </button>
            <button onclick="abrirModalPontoNovo('INTERRUPTOR'); toggleSpeedDialMobile();" class="bg-purple-600 hover:bg-purple-500 text-white font-bold py-1.5 px-3 rounded-xl shadow-lg flex items-center gap-2 text-xs border border-purple-400/40">
                <span>+ Interruptor</span> <i class="fa-solid fa-toggle-on text-xs"></i>
            </button>
            <button onclick="abrirModalNovoComodo(); toggleSpeedDialMobile();" class="bg-slate-800 hover:bg-slate-700 text-amber-400 font-bold py-1.5 px-3 rounded-xl shadow-lg flex items-center gap-2 text-xs border border-amber-500/40">
                <span>+ Novo Cômodo</span> <i class="fa-solid fa-cube text-xs"></i>
            </button>
        </div>

        <!-- Botão Principal do FAB -->
        <button id="btnPrincipalFabMobile" onclick="toggleSpeedDialMobile()" class="mobile-fab-btn w-13 h-13 p-3.5 bg-gradient-to-tr from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 rounded-full shadow-2xl flex items-center justify-center text-lg font-black transition active:scale-95 ring-4 ring-slate-950/80">
            <i id="iconeFabPrincipal" class="fa-solid fa-plus text-xl transition transform"></i>
        </button>
    </div>

    <!-- MOBILE BOTTOM NAVIGATION BAR (BARRA NATIVA INFERIOR COM AS 6 ABAS) -->
    <nav class="mobile-bottom-nav fixed bottom-0 left-0 right-0 z-40 bg-slate-900/95 backdrop-blur-xl border-t border-slate-800/90 shadow-2xl flex items-center justify-around px-1 py-1.5 text-slate-400 no-print safe-area-bottom">
        <button data-tab="planta" onclick="trocarAba('planta')" class="tab-btn-mobile text-amber-400 border-t-2 border-amber-400 bg-slate-850 flex flex-col items-center justify-center w-full py-1 rounded-lg transition active:scale-95">
            <i class="fa-solid fa-pen-ruler text-sm"></i>
            <span class="text-[9px] font-bold mt-0.5">Planta</span>
        </button>
        <button data-tab="instalacoes" onclick="trocarAba('instalacoes')" class="tab-btn-mobile flex flex-col items-center justify-center w-full py-1 rounded-lg transition active:scale-95">
            <i class="fa-solid fa-bolt-lightning text-sm"></i>
            <span class="text-[9px] font-medium mt-0.5">Elétrica</span>
        </button>
        <button data-tab="visualizacao3d" onclick="trocarAba('visualizacao3d')" class="tab-btn-mobile flex flex-col items-center justify-center w-full py-1 rounded-lg transition active:scale-95">
            <i class="fa-solid fa-cube text-sm"></i>
            <span class="text-[9px] font-medium mt-0.5">3D BIM</span>
        </button>
        <button data-tab="alimentador" onclick="trocarAba('alimentador')" class="tab-btn-mobile flex flex-col items-center justify-center w-full py-1 rounded-lg transition active:scale-95">
            <i class="fa-solid fa-microchip text-sm"></i>
            <span class="text-[9px] font-medium mt-0.5">Quadro</span>
        </button>
        <button data-tab="materiais" onclick="trocarAba('materiais')" class="tab-btn-mobile flex flex-col items-center justify-center w-full py-1 rounded-lg transition active:scale-95">
            <i class="fa-solid fa-boxes-stacked text-sm"></i>
            <span class="text-[9px] font-medium mt-0.5">Materiais</span>
        </button>
        <button data-tab="duvidas" onclick="trocarAba('duvidas')" class="tab-btn-mobile flex flex-col items-center justify-center w-full py-1 rounded-lg transition active:scale-95">
            <i class="fa-solid fa-circle-question text-sm"></i>
            <span class="text-[9px] font-medium mt-0.5">NBR 5410</span>
        </button>
    </nav>
"""

    # Inject mobile floating widgets before </body>
    old_body_end = '</body>'
    if old_body_end in html:
        html = html.replace(old_body_end, mobile_floating_widgets + "\n" + old_body_end, 1)
        print("Mobile FAB and Bottom Navigation Bar injected.")

    # =========================================================================
    # 5. FLOATING ZOOM CONTROLS ON CANVASES (FOR MOBILE/TOUCH ZOOM IN/OUT)
    # =========================================================================
    # On cadCanvas
    old_cad_canvas_div = '<div class="relative w-full overflow-hidden rounded-xl border-2 border-slate-800 bg-slate-950 shadow-inner">'
    new_cad_canvas_div = """<div class="relative w-full overflow-hidden rounded-xl border-2 border-slate-800 bg-slate-950 shadow-inner">
                        <!-- CONTROLES DE ZOOM / PAN NA TELA (OTIMIZADO PARA TOUCH & MOBILE) -->
                        <div class="absolute top-2 right-2 z-10 flex items-center gap-1 bg-slate-900/90 backdrop-blur-sm border border-slate-700/80 rounded-xl p-1 shadow-lg">
                            <button onclick="ajustarZoomCad(1.15)" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs flex items-center justify-center transition active:scale-90" title="Aumentar Zoom">
                                <i class="fa-solid fa-magnifying-glass-plus"></i>
                            </button>
                            <button onclick="ajustarZoomCad(0.87)" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs flex items-center justify-center transition active:scale-90" title="Diminuir Zoom">
                                <i class="fa-solid fa-magnifying-glass-minus"></i>
                            </button>
                            <button onclick="resetarZoomCad()" class="px-2 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 font-bold text-[10px] flex items-center justify-center transition active:scale-90" title="Centralizar e redefinir zoom padrão">
                                100%
                            </button>
                        </div>"""

    if old_cad_canvas_div in html:
        html = html.replace(old_cad_canvas_div, new_cad_canvas_div, 1)
        print("Zoom controls added to cadCanvas.")

    # On instalacoesCanvas
    old_inst_canvas_div = '<div class="relative w-full overflow-hidden rounded-2xl border-2 border-sky-950/70 bg-slate-950 shadow-2xl">'
    new_inst_canvas_div = """<div class="relative w-full overflow-hidden rounded-2xl border-2 border-sky-950/70 bg-slate-950 shadow-2xl">
                        <!-- CONTROLES DE ZOOM NA TELA DE INSTALAÇÕES (TOUCH / MOBILE) -->
                        <div class="absolute top-2 right-2 z-10 flex items-center gap-1 bg-slate-900/90 backdrop-blur-sm border border-slate-700/80 rounded-xl p-1 shadow-lg">
                            <button onclick="ajustarZoomCad(1.15)" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs flex items-center justify-center transition active:scale-90" title="Aumentar Zoom">
                                <i class="fa-solid fa-magnifying-glass-plus"></i>
                            </button>
                            <button onclick="ajustarZoomCad(0.87)" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs flex items-center justify-center transition active:scale-90" title="Diminuir Zoom">
                                <i class="fa-solid fa-magnifying-glass-minus"></i>
                            </button>
                            <button onclick="resetarZoomCad()" class="px-2 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 font-bold text-[10px] flex items-center justify-center transition active:scale-90" title="100%">
                                100%
                            </button>
                        </div>"""

    if old_inst_canvas_div in html:
        html = html.replace(old_inst_canvas_div, new_inst_canvas_div, 1)
        print("Zoom controls added to instalacoesCanvas.")

    # =========================================================================
    # 6. TOUCH EVENT HANDLERS & MOBILE JAVASCRIPT LOGIC
    # =========================================================================
    mobile_js_functions = """
        // =====================================================================
        // CONTROLADORES DE INTERFACE MOBILE & TOUCH
        // =====================================================================
        function abrirDrawerMobile() {
            const drawer = document.getElementById('drawerMenuMobile');
            if (drawer) drawer.classList.remove('hidden');
        }

        function fecharDrawerMobile() {
            const drawer = document.getElementById('drawerMenuMobile');
            if (drawer) drawer.classList.add('hidden');
        }

        function toggleSpeedDialMobile() {
            const items = document.getElementById('mobileSpeedDialItems');
            const icon = document.getElementById('iconeFabPrincipal');
            if (!items) return;
            const isHidden = items.classList.contains('hidden');
            if (isHidden) {
                items.classList.remove('hidden');
                items.classList.add('flex');
                if (icon) icon.className = 'fa-solid fa-xmark text-xl transition transform rotate-90';
            } else {
                items.classList.add('hidden');
                items.classList.remove('flex');
                if (icon) icon.className = 'fa-solid fa-plus text-xl transition transform';
            }
        }

        function alternarPavimentoMobile() {
            if (!state.pavimentos || state.pavimentos.length <= 1) return;
            const pIdx = state.pavimentos.findIndex(p => p.id === state.pavimentoAtivoId);
            const proxIdx = (pIdx + 1) % state.pavimentos.length;
            selecionarPavimento(state.pavimentos[proxIdx].id);

            const lbl = document.getElementById('lblNomePavimentoMobile');
            if (lbl) lbl.textContent = state.pavimentos[proxIdx].nome.replace('Pavimento ', '');
        }

        function ajustarZoomCad(fator) {
            state.escala = Math.max(15, Math.min(80, state.escala * fator));
            desenharCAD();
            desenharInstalacoes();
        }

        function resetarZoomCad() {
            state.escala = 35;
            desenharCAD();
            desenharInstalacoes();
        }

        // SUPORTE A TOQUE (TOUCH EVENTS) EM CANVASES 2D
        function vincularEventosTouchCanvas(canvasId, isInstalacoes = false) {
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;

            let lastTouchTime = 0;

            canvas.addEventListener('touchstart', (e) => {
                if (e.touches.length === 1) {
                    const t = e.touches[0];
                    const rect = canvas.getBoundingClientRect();
                    const scaleX = canvas.width / rect.width;
                    const scaleY = canvas.height / rect.height;
                    const mx = (t.clientX - rect.left) * (isInstalacoes ? scaleX : 1);
                    const my = (t.clientY - rect.top) * (isInstalacoes ? scaleY : 1);

                    // Detecção de Duplo Toque no Mobile
                    const now = Date.now();
                    if (now - lastTouchTime < 320) {
                        // Trata como Double Click
                        const comodosAndar = state.comodos.filter(c => c.pavimentoId === state.pavimentoAtivoId);
                        for (let c of comodosAndar) {
                            const cw = c.largura * state.escala;
                            const ch = c.comprimento * state.escala;
                            if (mx >= c.x && mx <= c.x + cw && my >= c.y && my <= c.y + ch) {
                                e.preventDefault();
                                abrirModalAdicionarPontoRapido(c, mx, my);
                                return;
                            }
                        }
                    }
                    lastTouchTime = now;

                    // Dispara mousedown simulado
                    const simulatedEvent = new MouseEvent('mousedown', {
                        clientX: t.clientX,
                        clientY: t.clientY,
                        bubbles: true
                    });
                    canvas.dispatchEvent(simulatedEvent);
                    e.preventDefault();
                }
            }, { passive: false });

            canvas.addEventListener('touchmove', (e) => {
                if (e.touches.length === 1) {
                    const t = e.touches[0];
                    const simulatedEvent = new MouseEvent('mousemove', {
                        clientX: t.clientX,
                        clientY: t.clientY,
                        bubbles: true
                    });
                    canvas.dispatchEvent(simulatedEvent);
                    e.preventDefault(); // Impede o scroll indesejado durante arraste
                }
            }, { passive: false });

            canvas.addEventListener('touchend', (e) => {
                const simulatedEvent = new MouseEvent('mouseup', { bubbles: true });
                canvas.dispatchEvent(simulatedEvent);
            }, { passive: false });
        }
    """

    # Inject mobile JS functions
    old_setup_nav = "function setupNavegacaoAbas() {"
    new_setup_nav = mobile_js_functions + """
        function setupNavegacaoAbas() {
            // Vincula touch nos canvases
            vincularEventosTouchCanvas('cadCanvas', false);
            vincularEventosTouchCanvas('instalacoesCanvas', true);
    """

    if old_setup_nav in html:
        html = html.replace(old_setup_nav, new_setup_nav, 1)
        print("Mobile Touch Event Handlers and setupNavegacaoAbas updated.")
    else:
        print("WARNING: function setupNavegacaoAbas() not found!")

    # In selecionarPavimento, update mobile badge
    old_sel_pav = "state.pavimentoAtivoId = pavId;"
    new_sel_pav = """state.pavimentoAtivoId = pavId;
            const pavAtualObj = state.pavimentos.find(p => p.id === pavId);
            if (pavAtualObj) {
                const lblMob = document.getElementById('lblNomePavimentoMobile');
                if (lblMob) lblMob.textContent = pavAtualObj.nome.replace('Pavimento ', '');
            }"""

    if old_sel_pav in html:
        html = html.replace(old_sel_pav, new_sel_pav, 1)
        print("selecionarPavimento updated with mobile badge sync.")

    # Save to index.html and sync to Projeto elétrico.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved index.html successfully! Final size:", len(html))

    with open('Projeto elétrico.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Synced to Projeto elétrico.html successfully!")

if __name__ == '__main__':
    run()
