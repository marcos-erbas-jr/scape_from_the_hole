import random
import pygame
import sys

def jogo_principal():
    pygame.init()

    # Tela
    LARGURA, ALTURA = 500, 353
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Escape the Hole")

    clock = pygame.time.Clock()

    # --- Cores ---
    PRETO = (0, 0, 0)
    LARANJA = (255, 140, 0)
    MARROM = (120, 80, 60)

    jogador_entrou_na_nave = False
    nave_voando = False
    vel_nave_y = 2  # velocidade de subida da nave

    tempo_total = 15  # segundos
    tempo_restante = tempo_total

    # --- Carregar animações ---
    idle_frames = [pygame.image.load(f"../Animation Idle/Idle{i}.png").convert_alpha() for i in range(1, 5)]
    run_frames = [pygame.image.load(f"../Run/Run{i}.png").convert_alpha() for i in range(1, 4)]

    idle_index = run_index = 0
    idle_tempo = run_tempo = 0
    frame_intervalo = 150  # ms entre frames
    direcao = "direita"

    # --- Player ---
    player = idle_frames[0].get_rect(midbottom=(100, ALTURA - 20))
    vel_x = vel_y = 0
    gravidade = 0.8
    
    no_chao = False

    # --- Energia ---
    energia = 0
    energia_max = 100

    # --- Plataformas ---
    ANDAR_ALTURA = 120
    NUM_ANDARES = 15
    andares = [pygame.Rect(0, ALTURA - 20 - (i * ANDAR_ALTURA), LARGURA, 20) for i in range(NUM_ANDARES)]
    andar_atual = 0

    # --- Nave ---
    nave_img = pygame.image.load(f"../Ship/ShipStatic1.png").convert_alpha()
    nave_frames = [
        pygame.image.load("../Ship/Ship1.png").convert_alpha(),
        pygame.image.load("../Ship/Ship2.png").convert_alpha()
    ]

    nave_index = 0
    nave_tempo = 0
    nave_frame_intervalo = 200  # ms entre frames

    # --- Cristais ---
    cristal_img = pygame.image.load(f"../Itens/Cristal.png").convert_alpha()
    cristais = []
    for i in range(len(andares)):
        if i == NUM_ANDARES - 1:
            # Último andar: colocar nave
            nave_rect = nave_img.get_rect(midbottom=(random.randint(50, LARGURA - 50), andares[i].top))
        else:
            x_aleatorio = random.randint(20, LARGURA - 20)
            c = cristal_img.get_rect(midbottom=(x_aleatorio, andares[i].top))
            cristais.append(c)

    # --- Barra de energia ---
    def desenhar_barra(x, y, largura, altura, valor, maximo):
        pygame.draw.rect(tela, (124, 99, 94), (x, y, largura, altura), 2)
        altura_interna = int((valor / maximo) * (altura - 4))
        pygame.draw.rect(tela, LARANJA, (x + 2, y + altura - 2 - altura_interna, largura - 4, altura_interna))

    # --- Câmera ---
    camera_y = 0
    scroll_vel = 5  # pixels por frame

    # --- Vitória ---
    you_win_img = pygame.image.load("../Win/WinGame.png").convert_alpha()
    you_win_img = pygame.transform.scale(you_win_img, (500, 353))
    tempo_inicio_voo = None
    mostrar_you_win = False
    delay_you_win = 3  # segundos depois de a nave começar a subir

    # --- Game Over ---
    game_over_img = pygame.image.load("../GameOver/GameOverFinal.png").convert_alpha()
    game_over_img = pygame.transform.scale(game_over_img, (500, 353))  # ajusta o tamanho
    game_over = False

    # Reiniciar jogo
    def mostrar_tela_final(tela, imagem):
        tempo_inicio = pygame.time.get_ticks()  # marca o tempo
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            tela.blit(imagem, (0, 0))
            pygame.display.flip()

            # verifica se passaram 5 segundos (5000 ms)
            if pygame.time.get_ticks() - tempo_inicio > 5000:
                rodando = False


    # --- Loop principal ---
    while True:
        dt = clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Se já deu Game Over -> mostra tela e encerra a função
        if game_over:
            mostrar_tela_final(tela, game_over_img)
            return  # sai de jogo_principal() e volta para tela_inicial()

        # Atualizar timer apenas se o jogador ainda não entrou na nave e não acabou o jogo
        if not jogador_entrou_na_nave and not game_over:
            tempo_restante -= dt / 1000  # dt está em ms, convertemos para segundos
            if tempo_restante <= 0:
                tempo_restante = 0
                game_over = True
                continue  # no próximo frame desenha tela de game over

        # --- Input ---
        teclas = pygame.key.get_pressed()
        vel_x = 0
        if teclas[pygame.K_LEFT]:
            vel_x = -5
        if teclas[pygame.K_RIGHT]:
            vel_x = 5


        # Atualizar direção
        if vel_x < 0:
            direcao = "esquerda"
        elif vel_x > 0:
            direcao = "direita"

        # --- Física ---
        vel_y += gravidade
        player.x += vel_x
        player.y += vel_y

        # Limite horizontal
        if player.left < 0:
            player.left = 0
        elif player.right > LARGURA:
            player.right = LARGURA

        # Colisão com plataformas
        no_chao = False
        for plat in andares:
            if player.colliderect(plat) and vel_y >= 0:
                player.bottom = plat.top
                vel_y = 0
                no_chao = True

        # Colisão com cristais
        for c in cristais:
            if player.colliderect(c):
                energia = energia_max
                c.x = -100  # remove cristal da tela

        # Colisão com a nave (último andar)
        if player.colliderect(nave_rect):
            jogador_entrou_na_nave = True
            nave_voando = True
            if tempo_inicio_voo is None:  # garante que só registra uma vez
                tempo_inicio_voo = pygame.time.get_ticks()

        # Consumir energia ao voar
        if teclas[pygame.K_SPACE] and energia > 0:
            vel_y = -4
            energia -= 7
            if energia < 0:
                energia = 0

        # Subir de andar automaticamente
        if player.top < andares[andar_atual].top - 100 and andar_atual < NUM_ANDARES - 1:
            andar_atual += 1

        # --- Animação ---
        if vel_x != 0:
            run_tempo += dt
            if run_tempo >= frame_intervalo:
                run_index = (run_index + 1) % len(run_frames)
                run_tempo = 0
            player_img = run_frames[run_index]
        else:
            idle_tempo += dt
            if idle_tempo >= frame_intervalo:
                idle_index = (idle_index + 1) % len(idle_frames)
                idle_tempo = 0
            player_img = idle_frames[idle_index]

        # Virar sprite
        if direcao == "esquerda":
            player_img = pygame.transform.flip(player_img, True, False)

        # --- Atualizar câmera ---
        if player.top - camera_y < ALTURA / 2:
            diff = (ALTURA / 2) - (player.top - camera_y)
            camera_y -= min(diff, scroll_vel)

        # --- Verificação de Objetivo ---
        if tempo_inicio_voo is not None and not mostrar_you_win:
            tempo_passado_voo = (pygame.time.get_ticks() - tempo_inicio_voo) / 1000  # em segundos
            if tempo_passado_voo >= delay_you_win:
                mostrar_you_win = True

        # --- Desenho ---
        tela.fill(PRETO)

        for i, plat in enumerate(andares):
            pygame.draw.rect(tela, MARROM, plat.move(0, -camera_y))
            if i < NUM_ANDARES - 1:  # todos menos o último
                tela.blit(cristal_img, (cristais[i].x, cristais[i].y - camera_y))

        # Nave
        if nave_voando:
            nave_tempo += dt
            if nave_tempo >= nave_frame_intervalo:
                nave_index = (nave_index + 1) % len(nave_frames)
                nave_tempo = 0
            nave_rect.y -= vel_nave_y
            tela.blit(nave_frames[nave_index], nave_rect.move(0, -camera_y))
        else:
            tela.blit(nave_img, nave_rect.move(0, -camera_y))

        # Player só se não entrou na nave
        if not jogador_entrou_na_nave:
            tela.blit(player_img, player.move(0, -camera_y))

        # Barra de energia
        desenhar_barra(20, 50, 20, 100, energia, energia_max)

        # Timer
        fonte = pygame.font.SysFont(None, 36)
        texto_timer = fonte.render(f"{int(tempo_restante)}", True, (255, 255, 255))
        texto_rect = texto_timer.get_rect(center=(LARGURA // 2, 30))
        tela.blit(texto_timer, texto_rect)

        # Se ganhou -> mostra tela e encerra a função
        if mostrar_you_win:
            mostrar_tela_final(tela, you_win_img)
            return

        pygame.display.flip()