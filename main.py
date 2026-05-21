"""
main.py — Entry point do LAZY AUDIO.
"""
import os
import sys

# Corrige ambiente se rodando com sudo no Linux
if sys.platform == "linux" and os.geteuid() == 0:
    sudo_uid = os.environ.get("SUDO_UID")
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_uid and sudo_user:
        os.environ.setdefault("XDG_RUNTIME_DIR", f"/run/user/{sudo_uid}")
        os.environ.setdefault("PULSE_SERVER", f"unix:/run/user/{sudo_uid}/pulse/native")
        if "WAYLAND_DISPLAY" not in os.environ:
            os.environ["WAYLAND_DISPLAY"] = "wayland-0"
        if "DISPLAY" not in os.environ:
            os.environ["DISPLAY"] = ":0"

from ui.app import LazyAudioApp


if __name__ == "__main__":
    app = LazyAudioApp()

    def ao_fechar():
        app.rodando = False
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", ao_fechar)
    app.mainloop()