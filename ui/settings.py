import os
import threading
import time
import keyboard
import customtkinter as ctk

from config import (
    BASE_DIR, COR_FUNDO, COR_CARD2, COR_BORDA,
    COR_ROXO, COR_ROXO_MED, COR_ROXO_GLOW,
    COR_TEXTO, COR_TEXTO_DIM, COR_ACCENT,
)
from ui.utils import aplicar_icone_janela


class SettingsWindow:
    def __init__(self, parent, tecla_var: ctk.StringVar, idioma_var: ctk.StringVar):
        self._parent     = parent
        self.tecla_var   = tecla_var
        self.idioma_var  = idioma_var
        self._capturando = False
        self._win: ctk.CTkToplevel | None = None
        self.btn_tecla: ctk.CTkButton | None = None

    def abrir(self):
        if self._win and self._win.winfo_exists():
            self._win.focus()
            return

        w = ctk.CTkToplevel(self._parent)
        self._win = w
        w.title("Configurações — LAZY AUDIO")
        w.geometry("420x400")
        w.configure(fg_color=COR_FUNDO)
        w.resizable(False, False)
        w.attributes("-topmost", True)

        aplicar_icone_janela(w, delay_ms=200)

        self._build_ui(w)

    def _build_ui(self, w: ctk.CTkToplevel):
        hdr = ctk.CTkFrame(w, fg_color=COR_CARD2, corner_radius=0, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(
            hdr, text="⚙️  Configurações",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COR_TEXTO,
        ).place(x=20, rely=0.5, anchor="w")

        ctk.CTkFrame(w, height=1, fg_color=COR_BORDA).pack(fill="x")

        body = ctk.CTkFrame(w, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=20)

        ctk.CTkLabel(body, text="IDIOMA DA VOZ",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=COR_TEXTO_DIM).pack(anchor="w", pady=(0, 6))

        ctk.CTkOptionMenu(
            body, variable=self.idioma_var,
            values=["Português", "Inglês", "Espanhol"],
            width=370, height=40, corner_radius=10,
            fg_color=COR_CARD2, button_color=COR_ROXO,
            button_hover_color=COR_ROXO_MED,
            dropdown_fg_color=COR_CARD2,
            dropdown_hover_color=COR_ROXO_GLOW,
        ).pack(pady=(0, 20))

        ctk.CTkLabel(body, text="TECLA DE ATIVAÇÃO",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=COR_TEXTO_DIM).pack(anchor="w", pady=(0, 6))

        self.btn_tecla = ctk.CTkButton(
            body,
            text=f"  {self.tecla_var.get().upper()}",
            command=self._iniciar_captura,
            width=370, height=44, corner_radius=10,
            fg_color=COR_ROXO, hover_color=COR_ROXO_MED,
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.btn_tecla.pack(pady=(0, 8))

        ctk.CTkLabel(
            body,
            text="Clique no botão acima e pressione a tecla desejada.",
            font=ctk.CTkFont(size=12), text_color=COR_TEXTO_DIM,
        ).pack()

        ctk.CTkLabel(w, text="by @kaiudiass",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#5a4f7a").pack(pady=(6, 10))

    def _iniciar_captura(self):
        if self._capturando:
            return
        self._capturando = True
        self.btn_tecla.configure(
            text="  PRESSIONE UMA TECLA...",
            fg_color=COR_CARD2, text_color=COR_ACCENT, hover_color=COR_CARD2,
        )
        threading.Thread(target=self._capturar_thread, daemon=True).start()

    def _capturar_thread(self):
        time.sleep(0.1)
        tecla = keyboard.read_event().name
        self._parent.after(0, lambda: self._finalizar_captura(tecla))

    def _finalizar_captura(self, tecla: str):
        self.tecla_var.set(tecla)
        if self._win and self._win.winfo_exists():
            self.btn_tecla.configure(
                text=f"  {tecla.upper()}",
                fg_color=COR_ROXO, text_color="white",
                hover_color=COR_ROXO_MED,
            )
        self._capturando = False
