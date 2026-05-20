import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

from config import COR_FUNDO, COR_ROXO, COR_ROXO_MED, COR_ROXO_GLOW, COR_VERMELHO
from ui.utils import carregar_imagem


def _hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


class MicCanvas(tk.Canvas):
    def __init__(self, parent, size: int = 150, raio_base: int = 42,
                 on_click=None, **kwargs):
        super().__init__(
            parent,
            width=size, height=size,
            bg=COR_FUNDO, highlightthickness=0,
            **kwargs,
        )
        self.SIZE        = size
        self.CENTRO      = size // 2
        self.RAIO_BASE   = raio_base
        self._on_click   = on_click

        self._animando       = False
        self._anim_raio      = float(raio_base)
        self._anim_crescendo = True
        self._pulso_raio     = 0.0

        self._circle_img_tk   = None
        self._circle_img_item = self.create_image(
            self.CENTRO, self.CENTRO, anchor="center", tags="clicavel"
        )

        self._carregar_icone_mic()
        self._render(self.RAIO_BASE, COR_ROXO, glow=True)

        self.tag_bind("clicavel", "<Button-1>", self._ao_clicar)
        self.tag_bind("clicavel", "<Enter>",    lambda e: self.config(cursor="hand2"))
        self.tag_bind("clicavel", "<Leave>",    lambda e: self.config(cursor="arrow"))

    def _carregar_icone_mic(self):
        img = carregar_imagem("icone_microfone.png", (30, 30))
        if img:
            self._img_mic_tk = ImageTk.PhotoImage(img)
            self._icon_item = self.create_image(
                self.CENTRO, self.CENTRO,
                image=self._img_mic_tk, tags="clicavel"
            )
        else:
            self._icon_item = self.create_text(
                self.CENTRO, self.CENTRO,
                text="🎙️", font=("Segoe UI Emoji", 22),
                fill="white", tags="clicavel"
            )

    def _render(self, raio: float, cor: str, glow: bool = False,
                anel_alpha: float = 0.0, anel_raio: float = 0.0,
                cor_glow: str = COR_ROXO_GLOW, cor_anel: str = COR_ROXO):
        S     = self.SIZE
        SCALE = 4
        cx    = cy = S * SCALE // 2

        img  = Image.new("RGBA", (S * SCALE, S * SCALE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if anel_alpha > 0 and anel_raio > 0:
            ra = int(anel_raio * SCALE)
            gr, gg, gb = _hex_to_rgb(cor_anel)
            a = int(anel_alpha * 180)
            draw.ellipse(
                [cx - ra, cy - ra, cx + ra, cy + ra],
                outline=(gr, gg, gb, a), width=max(1, SCALE * 2),
            )

        if glow:
            for offset, alpha in [(14, 30), (10, 55), (6, 80)]:
                rg = int((raio + offset) * SCALE)
                gr, gg, gb = _hex_to_rgb(cor_glow)
                draw.ellipse(
                    [cx - rg, cy - rg, cx + rg, cy + rg],
                    fill=(gr, gg, gb, alpha),
                )

        r = int(raio * SCALE)
        cr, cg, cb = _hex_to_rgb(cor)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(cr, cg, cb, 255))

        img = img.resize((S, S), Image.Resampling.LANCZOS)

        fr, fg_, fb = _hex_to_rgb(COR_FUNDO)
        bg = Image.new("RGBA", (S, S), (fr, fg_, fb, 255))
        bg.alpha_composite(img)

        self._circle_img_tk = ImageTk.PhotoImage(bg.convert("RGB"))
        self.itemconfig(self._circle_img_item, image=self._circle_img_tk)

    def _ao_clicar(self, _event=None):
        if self._on_click:
            self._on_click()

    def iniciar_animacao(self):
        self._animando       = True
        self._anim_raio      = float(self.RAIO_BASE)
        self._anim_crescendo = True
        self._pulso_raio     = 0.0
        self._tick()

    def parar_animacao(self, estado: str = "pronto"):
        self._animando = False
        cor = COR_ROXO_MED if estado == "processando" else COR_ROXO
        self._render(self.RAIO_BASE, cor, glow=True)

    def _tick(self):
        if not self._animando:
            return

        if self._anim_crescendo:
            self._anim_raio += 1.0
            if self._anim_raio >= self.RAIO_BASE + 10:
                self._anim_crescendo = False
        else:
            self._anim_raio -= 1.0
            if self._anim_raio <= self.RAIO_BASE - 3:
                self._anim_crescendo = True

        self._pulso_raio += 1.0
        if self._pulso_raio > 60:
            self._pulso_raio = 0.0
        alpha_anel = max(0.0, 1.0 - (self._pulso_raio / 60))
        raio_anel  = self.RAIO_BASE + self._pulso_raio

        self._render(
            self._anim_raio, COR_VERMELHO,
            glow=True,
            anel_alpha=alpha_anel,
            anel_raio=raio_anel,
            cor_glow="#b91c1c",
            cor_anel=COR_VERMELHO,
        )
        self.after(20, self._tick)
