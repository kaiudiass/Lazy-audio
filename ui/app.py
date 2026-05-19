import threading
import time
import keyboard
import customtkinter as ctk

from config import (
    COR_FUNDO, COR_CARD, COR_CARD2, COR_BORDA,
    COR_ROXO, COR_ROXO_MED, COR_ROXO_CLARO,
    COR_TEXTO, COR_TEXTO_DIM, COR_VERDE, COR_VERMELHO,
)
from ui.utils import carregar_imagem, aplicar_icone_janela
from ui.mic_canvas import MicCanvas
from ui.settings import SettingsWindow
from core import audio_recorder, transcriber


class LazyAudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LAZY AUDIO")
        self.geometry("460x530")
        self.configure(fg_color=COR_FUNDO)
        self.resizable(False, False)

        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "kaiudiass.lazyaudio.app.1.0"
            )
        except Exception:
            pass
        aplicar_icone_janela(self)

        self.microfones_dict: dict[str, int] = {}
        self.indice_selecionado: int | None  = None
        self.rodando       = True
        self.estado        = "carregando"
        self.tecla_var     = ctk.StringVar(value="right shift")
        self.idioma_var    = ctk.StringVar(value="Português")
        self.gravacao_via_clique = False

        self._fluxo_lock = threading.Lock()

        self._settings = SettingsWindow(self, self.tecla_var, self.idioma_var)

        self._build_ui()
        self._carregar_microfones()

        self._thread_teclado = threading.Thread(
            target=self._escutar_teclado, daemon=True
        )
        self._thread_teclado.start()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(14, 0))

        img_logo = carregar_imagem("logoinitial.png", (160, 38))
        if img_logo:
            logo_ctk = ctk.CTkImage(
                light_image=img_logo, dark_image=img_logo, size=img_logo.size
            )
            ctk.CTkLabel(header, text="", image=logo_ctk).pack(side="left")
        else:
            ctk.CTkLabel(
                header, text="LAZY AUDIO",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=COR_TEXTO,
            ).pack(side="left")

        img_eng = carregar_imagem("icone_engrenagem.png", (20, 20))
        if img_eng:
            icon_eng = ctk.CTkImage(
                light_image=img_eng, dark_image=img_eng, size=img_eng.size
            )
            btn_cfg = ctk.CTkButton(
                header, text="", image=icon_eng,
                width=38, height=38, corner_radius=10,
                fg_color=COR_CARD2, hover_color=COR_BORDA,
                border_width=1, border_color=COR_BORDA,
                command=self._settings.abrir,
            )
        else:
            btn_cfg = ctk.CTkButton(
                header, text="⚙️", width=38, height=38,
                corner_radius=10,
                fg_color=COR_CARD2, hover_color=COR_BORDA,
                command=self._settings.abrir,
            )
        btn_cfg.pack(side="right")

        ctk.CTkFrame(self, height=1, fg_color=COR_BORDA).pack(
            fill="x", padx=20, pady=(12, 0)
        )

        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.pack(expand=True, fill="both")

        self.badge_frame = ctk.CTkFrame(
            centro, fg_color=COR_CARD2, corner_radius=20,
            border_width=1, border_color=COR_BORDA,
        )
        self.badge_frame.pack(pady=(12, 0))

        self.badge_dot = ctk.CTkLabel(
            self.badge_frame, text="●",
            font=ctk.CTkFont(size=9), text_color=COR_TEXTO_DIM, width=12,
        )
        self.badge_dot.grid(row=0, column=0, padx=(10, 3), pady=6)

        self.lbl_status = ctk.CTkLabel(
            self.badge_frame, text="Carregando...",
            font=ctk.CTkFont(size=11, weight="bold"), text_color=COR_TEXTO_DIM,
        )
        self.lbl_status.grid(row=0, column=1, padx=(0, 10), pady=6)

        self.mic_canvas = MicCanvas(
            centro, size=150, raio_base=42, on_click=self._clique_gravar
        )
        self.mic_canvas.pack(pady=(8, 0))

        card = ctk.CTkFrame(
            centro, fg_color=COR_CARD2, corner_radius=12,
            border_width=1, border_color=COR_BORDA,
        )
        card.pack(fill="x", padx=20, pady=(10, 0))

        mic_row = ctk.CTkFrame(card, fg_color="transparent")
        mic_row.pack(fill="x", padx=12, pady=10)

        self.combo_var = ctk.StringVar(value="Buscando...")
        self.combo_mic = ctk.CTkOptionMenu(
            mic_row,
            variable=self.combo_var,
            command=self._ao_selecionar_microfone,
            height=30,
            fg_color=COR_CARD, button_color=COR_ROXO,
            button_hover_color=COR_ROXO_MED,
            font=ctk.CTkFont(size=11),
            dropdown_fg_color=COR_CARD2,
            dropdown_hover_color="#6d28d9",
            corner_radius=8,
        )
        self.combo_mic.pack(side="left", fill="x", expand=True)

        txt_frame = ctk.CTkFrame(
            self, fg_color=COR_CARD2, corner_radius=16,
            border_width=1, border_color=COR_BORDA,
        )
        txt_frame.pack(fill="x", padx=20, pady=(8, 0))

        txt_hdr = ctk.CTkFrame(txt_frame, fg_color="transparent")
        txt_hdr.pack(fill="x", padx=12, pady=(7, 2))
        ctk.CTkLabel(
            txt_hdr, text="ÚLTIMO TEXTO",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=COR_TEXTO_DIM,
        ).pack(side="left")

        self.btn_copiar = ctk.CTkButton(
            txt_hdr, text="Copiar",
            width=58, height=22, corner_radius=6,
            fg_color=COR_CARD, hover_color=COR_BORDA,
            border_width=1, border_color=COR_BORDA,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COR_TEXTO_DIM,
            command=self._copiar_texto,
        )
        self.btn_copiar.pack(side="right")

        self.textbox = ctk.CTkTextbox(
            txt_frame, height=100, corner_radius=8,
            fg_color=COR_CARD, text_color=COR_TEXTO,
            font=ctk.CTkFont(size=12), border_width=0,
        )
        self.textbox.pack(fill="x", padx=10, pady=(0, 8))
        self.textbox.insert("0.0", "Seu áudio ditado aparecerá aqui...")
        self.textbox.configure(state="disabled")

        ctk.CTkLabel(
            self, text="by @kaiudiass",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#5a4f7a",
        ).pack(pady=(6, 10))

    def _atualizar_status(self, texto: str, cor: str = COR_TEXTO_DIM):
        def _up():
            self.lbl_status.configure(text=texto, text_color=cor)
            dot_cor = (
                "#ef4444" if cor in (COR_ROXO_MED, COR_ROXO_CLARO)
                else COR_VERDE if cor == COR_VERDE
                else COR_TEXTO_DIM
            )
            self.badge_dot.configure(text_color=dot_cor)
        self.after(0, _up)

    def _copiar_texto(self):
        import pyperclip
        self.textbox.configure(state="normal")
        texto = self.textbox.get("0.0", "end").strip()
        self.textbox.configure(state="disabled")

        if not texto or texto == "Seu áudio ditado aparecerá aqui...":
            return

        pyperclip.copy(texto)
        self.btn_copiar.configure(text="Copiado!", text_color=COR_VERDE,
                                   border_color=COR_VERDE)
        self.after(1500, lambda: self.btn_copiar.configure(
            text="Copiar", text_color=COR_TEXTO_DIM, border_color=COR_BORDA
        ))

    def _set_historico(self, texto: str):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", texto)
        self.textbox.configure(state="disabled")

    def _carregar_microfones(self):
        mics = audio_recorder.listar_microfones()
        self.microfones_dict = mics
        nomes = list(mics.keys())

        if nomes:
            self.combo_mic.configure(values=nomes)
            fifine = next((n for n in nomes if "fifine" in n.lower()), None)
            selecionado = fifine or nomes[0]
            self.combo_var.set(selecionado)
            self.indice_selecionado = mics[selecionado]
            self.estado = "pronto"
            self._atualizar_status("Pronto para gravar", COR_VERDE)
        else:
            self.combo_mic.configure(values=["Sem dispositivo"])
            self.combo_var.set("Sem dispositivo")
            self.estado = "erro"
            self._atualizar_status("Erro de áudio", COR_VERMELHO)

    def _ao_selecionar_microfone(self, selecionado: str):
        self.indice_selecionado = self.microfones_dict.get(selecionado)
        if self.estado != "erro":
            self._atualizar_status("Pronto para gravar", COR_VERDE)

    def _clique_gravar(self):
        if self.estado == "pronto":
            self.gravacao_via_clique = True
            threading.Thread(target=self._fluxo, daemon=True).start()
        elif self.estado == "gravando" and self.gravacao_via_clique:
            self.gravacao_via_clique = False

    def _fluxo(self):
        if not self._fluxo_lock.acquire(blocking=False):
            return
        try:
            self._executar_fluxo()
        finally:
            self._fluxo_lock.release()

    def _executar_fluxo(self):
        if self.indice_selecionado is None:
            self._atualizar_status("Selecione o microfone", COR_VERMELHO)
            self.gravacao_via_clique = False
            return

        self.estado = "gravando"
        dica = "Clique para parar" if self.gravacao_via_clique else "Solte a tecla para parar"
        self._atualizar_status(f"Gravando... ({dica})", COR_ROXO_CLARO)
        self.after(0, self.mic_canvas.iniciar_animacao)

        tecla_atual = self.tecla_var.get()

        def continuar_gravando() -> bool:
            return keyboard.is_pressed(tecla_atual) or self.gravacao_via_clique

        sucesso = audio_recorder.gravar(
            self.indice_selecionado,
            tecla_fn=continuar_gravando,
        )

        self.estado = "processando"
        self._atualizar_status("Processando IA...", COR_ROXO_CLARO)
        self.after(0, lambda: self.mic_canvas.parar_animacao("processando"))

        if not sucesso:
            self.estado = "pronto"
            self._atualizar_status("Pronto para gravar", COR_VERDE)
            self.after(0, lambda: self.mic_canvas.parar_animacao("pronto"))
            return

        texto = transcriber.transcrever(self.idioma_var.get())
        if texto:
            transcriber.digitar_texto(texto)
            self.after(0, lambda: self._set_historico(texto))

        self.estado = "pronto"
        self._atualizar_status("Pronto para gravar", COR_VERDE)
        self.after(0, lambda: self.mic_canvas.parar_animacao("pronto"))

    def _escutar_teclado(self):
        while self.rodando:
            if self.estado == "pronto" and not self._settings._capturando:
                tecla = self.tecla_var.get()
                try:
                    if keyboard.is_pressed(tecla):
                        threading.Thread(target=self._fluxo, daemon=True).start()
                        while keyboard.is_pressed(tecla):
                            time.sleep(0.05)
                except Exception:
                    pass
            time.sleep(0.05)
