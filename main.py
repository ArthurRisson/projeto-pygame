import pygame
import random
import os
import math
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
import json
import speech_recognition as sr
import pyttsx3
from recursos.funcoes import tela_inicial
from recursos.funcoes import obter_nome_por_voz
from recursos.funcoes import falar
import sys
from recursos.funcoes import carregar_asset
voz = pyttsx3.init()
voz.setProperty("rate", 150)
pygame.init()  # inicializa todos os módulos do pygame, incluindo o mixer
# ou, se quiser só inicializar o mixer:
pygame.mixer.init()


inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Sobrevivente do Trânsito")
icone = pygame.image.load(carregar_asset("icone_min.png"))
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
iron = pygame.image.load(carregar_asset("iron.png"))


iron = pygame.transform.scale(iron, (80,80))
fundoStart = pygame.image.load(carregar_asset("fundoStart.png"))

fundoJogo = pygame.image.load(carregar_asset("fundoJogo.png"))

fundoDead = pygame.image.load(carregar_asset("fundomorte.png"))

missel = pygame.image.load(carregar_asset("missile.png"))


missel = pygame.transform.scale(missel, (215, 150))
ovelha = pygame.image.load(carregar_asset("ovelha.png"))


ovelha = pygame.transform.scale(ovelha, (60,60))
fundo_boas_vindas = pygame.image.load(carregar_asset("bemvindo.png"))

missileSound = pygame.mixer.Sound(carregar_asset("carro.wav"))

explosaoSound = pygame.mixer.Sound(carregar_asset("explo.wav"))



fonteMenu = pygame.font.SysFont("celeste",28)

fonteMorte = pygame.font.SysFont("celeste",120)

pygame.mixer.music.load(carregar_asset("somfundo.mp3"))

velocidadeOvelha = random.choice([2, -2])
def jogar():
    global nome  # Para ser acessado em outras funções
    posicaoXOvelha = 50
    posicaoYOvelha = 20
    velocidadeOvelha = random.choice([2, -2])

    usar_voz = messagebox.askyesno("Entrada de Nome", "Deseja usar o microfone para dizer seu nome?")

    if usar_voz:
        instrucoes_voz = (
            "Desvie dos carros!\n"
            "Mova para frente e para trás\n"
            "Se bater, você perde!\n"
            "Diga seu nickname quando ouvir o bip."
        )
        
        messagebox.showinfo("Instruções", instrucoes_voz) 
        
        nome = obter_nome_por_voz()
        if not nome:
            messagebox.showwarning("Aviso", "Não entendi. Tente novamente!")
            return
    else:
        root = tk.Tk()
        root.title("Informe seu nickname")

        largura_janela = 300
        altura_janela = 200
        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        def obter_nome():
            nonlocal root
            global nome
            nome = entry_nome.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
            else:
                root.destroy()

        instrucoes = "🚗 Desvie dos carros!\n⬆️⬇️ Mova para frente e para trás\n❌ Se bater, você perde!\n\nEscreva seu nickname:"
        label_instrucao = tk.Label(root, text=instrucoes, font=("Arial", 11))
        label_instrucao.pack(pady=10)

        entry_nome = tk.Entry(root)
        entry_nome.pack()

        botao = tk.Button(root, text="Enviar", command=obter_nome)
        botao.pack()

        root.mainloop()
    
    
    raio_bola = 30
    crescendo = True
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXMissel = -100
    posicaoYMissel = random.choice([120,220, 320, 420])
    velocidadeMissel = 1
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    larguraPersona = 80
    alturaPersona = 80
    larguaMissel  = 215
    alturaMissel  = 150
    dificuldade  = 30
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -15
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = 15
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pause()
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 165 :
            posicaoXPersona = 180
        elif posicaoXPersona >750:
            posicaoXPersona = 740
            
        if posicaoYPersona < 100 :
            posicaoYPersona = 100
        elif posicaoYPersona > 480:
            posicaoYPersona = 480
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( iron, (posicaoXPersona, posicaoYPersona) )
        if crescendo:
            raio_bola += 0.5
            if raio_bola >= 40:
                crescendo = False
        else:
            raio_bola -= 0.5
            if raio_bola <= 30:
                crescendo = True
        pygame.draw.circle(tela, (0, 0, 200), (900,50 ), int(raio_bola))
        
        posicaoXMissel = posicaoXMissel + velocidadeMissel
        if posicaoXMissel > 1000:
            posicaoXMissel = -100
            posicaoYMissel = random.choice([120, 220, 320, 420])
            pontos += 1
            velocidadeMissel += 1
            pygame.mixer.Sound.play(missileSound)
            
            
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        texto = fonteMenu.render("Presione *P* para pausar", True,branco)
        tela.blit(texto, (30,30))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))
        
        os.system("cls")
        # print( len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        posicaoXOvelha += velocidadeOvelha

# Se bater na borda, muda de direção
        if posicaoXOvelha <= 0 or posicaoXOvelha >= 900:
            velocidadeOvelha *= -1  # Inverte a direção
            posicaoYOvelha = random.randint(100, 600)  # Muda um pouco no eixo Y
        tela.blit(ovelha, (posicaoXOvelha, posicaoYOvelha))
        pygame.display.update()
        relogio.tick(60)

def pause():
    pausado = True
    textoPause = fonteMenu.render("Jogo Pausado - Pressione P para continuar", True, branco)

    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausado = False
        
        tela.blit(textoPause, (200, 300))
        pygame.display.update()
        relogio.tick(5)
def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    

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
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart = 40
    larguraButtonQuit = 150
    alturaButtonQuit = 40

    # Carrega os dados do arquivo
    
    if os.path.exists("log.dat"):
        with open("log.dat", "r") as arquivo:
            log_partidas = json.load(arquivo)
    else:
        log_partidas = {}

    ultimos_logs = list(log_partidas.items())[-5:]  # pega os 5 últimos registros

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit = 35

            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit = 40
                    quit()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))

        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 12))

        quitButton = pygame.draw.rect(tela, branco, (10, 60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25, 62))

        titulo = fonteMenu.render("🦶 Fim de Jogo - Últimos 5 Registros", True, branco)
        tela.blit(titulo, (350, 100))

        y_offset = 160
        for nick, dados in ultimos_logs:
            pontos, data = dados
            linha = fonteMenu.render(f"{nick}: {pontos} pts - {data}", True, branco)
            tela.blit(linha, (350, y_offset))
            y_offset += 40

        pygame.display.update()
        relogio.tick(60)


start()

