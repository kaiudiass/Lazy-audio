"""
Abstração de teclado multiplataforma.
- Usa 'keyboard' em ambos os sistemas (no Linux, exige root).
"""
import keyboard as _kb

def is_pressed(key: str) -> bool:
    try:
        return _kb.is_pressed(key)
    except Exception:
        return False

def send_paste() -> None:
    _kb.send("ctrl+v")

def read_key() -> str:
    return _kb.read_event().name
