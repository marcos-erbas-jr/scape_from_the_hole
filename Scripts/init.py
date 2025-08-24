import pygame
import sys
import levels   # importa o arquivo levels.py

pygame.init()

# Configurações da tela
largura, altura = 500, 353
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Escape the Hole")
icon = pygame.image.load('../Icon/Icon.png')
pygame.display.set_icon(icon)

# Carregar imagens
frame1 = pygame.image.load("../Model/Screen0.png").convert_alpha()
frame2 = pygame.image.load("../Model/Screen1.png").convert_alpha()
frames = [frame1, frame2]
frame_index = 0
frame_tempo = 0
frame_intervalo = 500  # troca a cada 1 segundo

# Tela de instruções
instrucoes_img = pygame.image.load("../Model/TelaInstrucao.png").convert_alpha()

relogio = pygame.time.Clock()


def tela_inicial():
    global frame_index, frame_tempo

    rodando = True
    while rodando:
        tempo_decorrido = relogio.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # quando apertar Enter
                    rodando = False
                    tela_instrucoes()  # chama tela de instruções

        # Troca de frame
        frame_tempo += tempo_decorrido
        if frame_tempo >= frame_intervalo:
            frame_index = (frame_index + 1) % len(frames)
            frame_tempo = 0

        # Desenha
        tela.blit(frames[frame_index], (0, 0))
        pygame.display.flip()


def tela_instrucoes():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Enter começa o jogo
                    rodando = False
                    levels.jogo_principal()  # inicia o jogo

        tela.blit(instrucoes_img, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    while True:
        tela_inicial()