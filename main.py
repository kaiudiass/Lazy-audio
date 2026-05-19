"""
main.py — Entry point do LAZY AUDIO.
"""
from ui.app import LazyAudioApp


if __name__ == "__main__":
    app = LazyAudioApp()

    def ao_fechar():
        app.rodando = False
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", ao_fechar)
    app.mainloop()