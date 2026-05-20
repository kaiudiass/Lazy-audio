import time
import pyperclip
import keyboard
from faster_whisper import WhisperModel

from config import ARQUIVO_AUDIO

_modelo = WhisperModel("small", device="cpu", compute_type="int8")

IDIOMAS = {
    "Português": "pt",
    "Inglês":    "en",
    "Espanhol":  "es",
}


def transcrever(idioma_nome: str) -> str:
    codigo = IDIOMAS.get(idioma_nome, "pt")
    segments, _ = _modelo.transcribe(ARQUIVO_AUDIO, language=codigo, vad_filter=True)
    return "".join(s.text for s in segments).strip()


def digitar_texto(texto: str) -> None:
    pyperclip.copy(texto + " ")
    time.sleep(0.1)
    keyboard.send("ctrl+v")
