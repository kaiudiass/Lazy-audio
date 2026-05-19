import os
import customtkinter as ctk

ctk.set_appearance_mode("Dark")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
ARQUIVO_AUDIO = os.path.join(TEMP_DIR, "fala_temporaria.wav")

os.makedirs(TEMP_DIR, exist_ok=True)

COR_FUNDO      = "#0a0a0f"
COR_CARD       = "#12111a"
COR_CARD2      = "#1a1826"
COR_BORDA      = "#2a2440"
COR_ROXO       = "#7c3aed"
COR_ROXO_MED   = "#8b5cf6"
COR_ROXO_CLARO = "#a78bfa"
COR_ROXO_GLOW  = "#6d28d9"
COR_TEXTO      = "#e2e8f0"
COR_TEXTO_DIM  = "#94a3b8"
COR_ACCENT     = "#c4b5fd"
COR_VERDE      = "#10b981"
COR_VERMELHO   = "#ef4444"
