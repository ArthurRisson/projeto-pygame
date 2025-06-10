import cx_Freeze
from cx_Freeze import setup, Executable

executaveis = [
    Executable(script="main.py", icon="icone.ico")
]

setup(
    name="Sobrevivente no Trânsito",
    version="1.0",
    description="Jogo com Pygame, Reconhecimento de Voz e Síntese",
    options={
        "build_exe": {
            "packages": ["pygame", "speech_recognition", "pyttsx3", "tkinter", "json", "os", "sys"],
            "includes": ["aifc", "chunk", "audioop", "pyttsx3.drivers", "pyttsx3.drivers.sapi5"],
            "excludes": ["audioloop"],
            "include_files": [
                ("assets","assets"),                # Pasta de imagens e sons
                "log.dat",               # Banco de dados local
                ("recursos","recursos"),
                "icone.ico"              # Suas funções personalizadas
            ]
        }
    },
    executables=executaveis
)