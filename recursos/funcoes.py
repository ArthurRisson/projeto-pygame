import os, time
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import pygame
import speech_recognition as sr
import pyttsx3
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Sobrevivente do Trânsito")
icone  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
iron = pygame.image.load("assets/iron.png")
iron = pygame.transform.scale(iron, (80,80))
fundoStart = pygame.image.load("assets/fundoStart.png")
fundoJogo = pygame.image.load("assets/fundoJogo.png")
fundoDead = pygame.image.load("assets/fundomorte.png")
missel = pygame.image.load("assets/missile.png")
missel = pygame.transform.scale(missel, (215, 150))
fundo_boas_vindas = pygame.image.load("assets/bemvindo.png")
pygame.init()
pygame.mixer.init()
missileSound = pygame.mixer.Sound("assets/carro.wav")
explosaoSound = pygame.mixer.Sound("assets/boom.aiff")
fonteMenu = pygame.font.SysFont("celeste",28)
fonteMorte = pygame.font.SysFont("celeste",120)
pygame.mixer.music.load("assets/somfundo.mp3")
voz = pyttsx3.init()
def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("log.dat","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("log.dat","w")
    
def escreverDados(nome, pontos):
    try:
        with open("log.dat", "r") as banco:
            conteudo = banco.read()
            if conteudo.strip() == "":
                dadosDict = {}
            else:
                dadosDict = json.loads(conteudo)
    except FileNotFoundError:
        dadosDict = {}  # Se o arquivo não existir, começa vazio

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dadosDict[nome] = (pontos, data_hora)

    with open("log.dat", "w") as banco:
        banco.write(json.dumps(dadosDict, indent=4, ensure_ascii=False))
    
    # END - inserindo no arquivo

def tela_boas_vindas():
    global nome  # Para usar em outras funções

    # Criar janela Tkinter
    root = tk.Tk()
    root.title("Boas-vindas ao Sobrevivente do Trânsito")
    root.geometry("400x300")
    root.resizable(False, False)

    # Título
    label_titulo = tk.Label(root, text="Bem-vindo ao Sobrevivente do Trânsito!", font=("Arial", 14, "bold"))
    label_titulo.pack(pady=10)

    # Instruções
    instrucoes = "🚗 Desvie dos carros!\n⬆️⬇️ Mova para frente e para trás\n❌ Se bater, você perde!\n"
    label_instrucao = tk.Label(root, text=instrucoes, font=("Arial", 11))
    label_instrucao.pack(pady=10)

    # Entrada de nome
   

    # Função para obter nome e fechar janela
    def iniciar_jogo():
        global nome
        nome = entry_nome.get().strip()
        if nome == "":
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()  # Fecha a janela

    # Botão iniciar
    botao_iniciar = tk.Button(root, text="Iniciar Jogo", font=("Arial", 12, "bold"), command=iniciar_jogo)
    botao_iniciar.pack(pady=15)

    root.mainloop()
    
def dead():
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(explosaoSound)
larguraButtonStart = 150
alturaButtonStart  = 40
larguraButtonQuit = 150
alturaButtonQuit  = 40
    
    # Carregar e processar o log
try:
    with open("log.dat", "r") as arquivo:
        log_partidas = json.load(arquivo)
except Exception as e:
    log_partidas = {}
    
    registros = list(log_partidas.items())[-5:]  # últimos 5 registros
    
    fonteLog = pygame.font.SysFont("celeste", 24)
    fonteTitulo = pygame.font.SysFont("celeste", 36)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
        
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        
        # Título
        titulo = fonteTitulo.render("Log das Últimas 5 Partidas", True, preto)
        tela.blit(titulo, (300, 20))
        
        # Mostrar cada registro do log
        y_inicio = 80
        espacamento = 40
        if registros:
            for i, (nome_jogador, dados) in enumerate(registros):
                pontos = dados[0]
                data = dados[1]
                texto_log = f"{i+1}. Jogador: {nome_jogador} | Pontos: {pontos} | Data: {data}"
                texto_render = fonteLog.render(texto_log, True, preto)
                tela.blit(texto_render, (50, y_inicio + i * espacamento))
        else:
            msg = fonteLog.render("Nenhum registro de partidas encontrado.", True, preto)
            tela.blit(msg, (50, y_inicio))
        
        # Botões
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)

def tela_inicial():
    tela.fill((0, 100, 200))
    nome = ""
    ativo = True

    input_box = pygame.Rect(350, 250, 300, 50)
    cor_ativo = (200, 200, 200)
    cor_inativo = (255, 255, 255)
    cor = cor_inativo

    larguraBotao = 250
    alturaBotao = 50
    botaoComecar = pygame.Rect(375, 500, larguraBotao, alturaBotao)

    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(evento.pos):
                    cor = cor_ativo
                else:
                    cor = cor_inativo

                if botaoComecar.collidepoint(evento.pos):
                    if nome != "":
                        return nome  # Começa o jogo
                    else:
                        print("Digite seu nome!")

            if evento.type == pygame.KEYDOWN:
                if cor == cor_ativo:
                    if evento.key == pygame.K_RETURN:
                        if nome != "":
                            return nome
                        else:
                            print("Digite seu nome!")
                    elif evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        if len(nome) < 15:  # Limite de caracteres
                            nome += evento.unicode

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))

        # Título
        titulo = fonteMenu.render("🚦 Sobrevivente do Trânsito 🚦", True, preto)
        tela.blit(titulo, (250, 350))

        # Instruções
        linhas = [
            "Desvie dos carros! 🚗💨",
            "⬆️⬇️ movem para cima e para baixo.",
            "❌ Se bater, você perde!",
            "Digite seu nome para começar:"
        ]

        for i, linha in enumerate(linhas):
            texto = fonteMenu.render(linha, True, preto)
            tela.blit(texto, (200, 350 + i * 40))

        # Caixa de texto
        pygame.draw.rect(tela, cor, input_box, border_radius=10)
        texto_nome = fonteMenu.render(nome, True, preto)
        tela.blit(texto_nome, (input_box.x + 10, input_box.y + 10))

        # Botão começar
        pygame.draw.rect(tela, branco, botaoComecar, border_radius=15)
        texto_botao = fonteMenu.render("Começar Jogo", True, preto)
        tela.blit(texto_botao, (botaoComecar.x + 30, botaoComecar.y + 10))

        pygame.display.update()
        relogio.tick(60)

def falar(texto):
    voz.say(texto)
    voz.runAndWait()

def obter_nome_por_voz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        falar("Diga seu nome, bip")
        print("🎤 Ouvindo nome...")
        audio = r.listen(source)
        try:
            nome = r.recognize_google(audio, language="pt-BR")
            falar(f"Você disse {nome}. Nome registrado.")
            return nome
        except sr.UnknownValueError:
            falar("Desculpe, não entendi. Tente novamente.")
            return obter_nome_por_voz()
        except sr.RequestError:
            falar("Erro ao se conectar com o serviço de voz.")
            return "Jogador"
