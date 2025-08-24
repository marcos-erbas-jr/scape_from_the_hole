import pygame
import sys

pygame.init()

# Tela
LARGURA, ALTURA = 500, 353
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Scape from the Hole")

clock = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
LARANJA = (255, 140, 0)
VERDE = (0, 255, 0)

# Player
player_img = pygame.Surface((20, 30))  # placeholder (trocar pelo sprite)
player_img.fill(BRANCO)
player = player_img.get_rect(midbottom=(100, ALTURA - 20))

vel_x = 0
vel_y = 0
gravidade = 0.8
pulo = -12
no_chao = False

# Energia
energia = 0
energia_max = 100

# Cristal
cristal_img = pygame.Surface((15, 15))
cristal_img.fill(LARANJA)
cristal = cristal_img.get_rect(midbottom=(400, ALTURA - 20))

# Função desenhar barra
def desenhar_barra(x, y, largura, altura, valor, maximo):
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 2)  # borda
    altura_interna = int((valor / maximo) * (altura - 4))
    pygame.draw.rect(tela, LARANJA, (x + 2, y + altura - 2 - altura_interna, largura - 4, altura_interna))

# Loop principal
while True:
    clock.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input
    teclas = pygame.key.get_pressed()
    vel_x = 0
    if teclas[pygame.K_LEFT]:
        vel_x = -5
    if teclas[pygame.K_RIGHT]:
        vel_x = 5
    if teclas[pygame.K_SPACE] and no_chao:
        vel_y = pulo
        no_chao = False
    # voo se tiver energia cheia
    if teclas[pygame.K_UP] and energia == energia_max:
        vel_y = -5

    # Física
    vel_y += gravidade
    player.x += vel_x
    player.y += vel_y

    # Colisão com o "chão"
    if player.bottom >= ALTURA - 20:
        player.bottom = ALTURA - 20
        vel_y = 0
        no_chao = True

    # Colisão com cristal
    if player.colliderect(cristal):
        energia = energia_max
        # cristal some depois de coletado
        cristal.x = -100

    # Desenho
    tela.fill(PRETO)
    tela.blit(player_img, player)
    tela.blit(cristal_img, cristal)

    # Barra de energia
    desenhar_barra(20, 50, 20, 100, energia, energia_max)

    pygame.display.flip()