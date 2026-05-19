import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.audio_recorder import listar_microfones

if __name__ == "__main__":
    mics = listar_microfones()
    if not mics:
        print("Nenhum microfone encontrado.")
    else:
        print(f"{'Índice':<8} Nome")
        print("-" * 50)
        for nome, idx in mics.items():
            print(f"{idx:<8} {nome}")
