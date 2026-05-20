"""
Abstração de teclado multiplataforma.
- Windows: usa 'keyboard' (funciona normalmente).
- Linux:   usa 'pynput' via X11 (não exige root).
"""
import sys

if sys.platform == "win32":
    import keyboard as _kb

    def is_pressed(key: str) -> bool:
        try:
            return _kb.is_pressed(key)
        except Exception:
            return False

    def send_paste() -> None:
        _kb.send("ctrl+v")

else:
    from pynput import keyboard as _pynput_kb
    from pynput.keyboard import Key, KeyCode, Controller

    _pressed: set = set()
    _controller = Controller()

    _KEY_MAP: dict = {
        "right shift": Key.shift_r,
        "left shift":  Key.shift_l,
        "right ctrl":  Key.ctrl_r,
        "left ctrl":   Key.ctrl_l,
        "right alt":   Key.alt_r,
        "left alt":    Key.alt_l,
        "shift":       Key.shift,
        "ctrl":        Key.ctrl,
        "alt":         Key.alt,
        "caps lock":   Key.caps_lock,
        "tab":         Key.tab,
        "enter":       Key.enter,
        "space":       Key.space,
        "backspace":   Key.backspace,
        "delete":      Key.delete,
        "esc":         Key.esc,
        "escape":      Key.esc,
        "f1":  Key.f1,  "f2":  Key.f2,  "f3":  Key.f3,  "f4": Key.f4,
        "f5":  Key.f5,  "f6":  Key.f6,  "f7":  Key.f7,  "f8": Key.f8,
        "f9":  Key.f9,  "f10": Key.f10, "f11": Key.f11, "f12": Key.f12,
    }

    def _on_press(key):
        _pressed.add(key)

    def _on_release(key):
        _pressed.discard(key)

    _listener = _pynput_kb.Listener(on_press=_on_press, on_release=_on_release)
    _listener.daemon = True
    _listener.start()

    def is_pressed(key: str) -> bool:
        target = _KEY_MAP.get(key.lower())
        if target is not None:
            return target in _pressed
        # Tecla de caractere simples
        try:
            return KeyCode.from_char(key) in _pressed
        except Exception:
            return False

    def send_paste() -> None:
        with _controller.pressed(Key.ctrl):
            _controller.tap('v')
