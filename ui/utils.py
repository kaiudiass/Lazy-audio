import os
import sys
from PIL import Image, ImageOps, ImageTk

from config import BASE_DIR


def carregar_imagem(nome: str, tamanho_max: tuple | None = None) -> Image.Image | None:
    caminho = os.path.join(BASE_DIR, "image", nome)
    if not os.path.exists(caminho):
        return None
    img = Image.open(caminho).convert("RGBA")
    if tamanho_max:
        img = ImageOps.contain(img, tamanho_max, Image.Resampling.LANCZOS)
    return img


def aplicar_icone_janela(janela, ico_nome: str = "logodoappicone.ico",
                          png_nome: str = "logodoappicone.png",
                          delay_ms: int = 0) -> None:
    caminho_ico = os.path.join(BASE_DIR, "image", ico_nome)

    def _aplicar():
        if sys.platform == "win32" and os.path.exists(caminho_ico):
            janela.iconbitmap(caminho_ico)
        else:
            img = carregar_imagem(png_nome)
            if img:
                tk_img = ImageTk.PhotoImage(img)
                janela.wm_iconphoto(True, tk_img)
                janela._icon_ref = tk_img

    if delay_ms > 0:
        janela.after(delay_ms, _aplicar)
    else:
        _aplicar()
