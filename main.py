import pygame
import random
import sys

pygame.init()

# Vista cuadro principal del juego
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquiva el Enemigo")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Imagenes de jugadores
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
player_img_2 = pygame.image.load("player2.png")  # avión mejorado

# Escalado de imagenes
player_size = 100
enemy_size = 100
player_img = pygame.transform.scale(player_img, (player_size, player_size))
player_img_2 = pygame.transform.scale(player_img_2, (player_size, player_size))
enemy_img = pygame.transform.scale(enemy_img, (enemy_size, enemy_size))

# Posiciones iniciales
player_pos = [WIDTH // 2, HEIGHT - player_size]
player_speed = 5

enemy_speed = 7
enemies = []

# Bala
bullets = []
bullet_speed = 10

# Estados
clock = pygame.time.Clock()
is_paused = False
bombs = 0
upgrade = False

# Función de colisión
def detect_collision(pos1, size1, pos2, size2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (
        x1 < x2 + size2 and x1 + size1 > x2 and
        y1 < y2 + size2 and y1 + size1 > y2
    )

def spawn_enemy():
    return [random.randint(0, WIDTH - enemy_size), 0]

def game_loop():
    global is_paused, bombs, upgrade, player_img

    running = True
    score = 0
    enemies.append(spawn_enemy())

    while running:
        if not is_paused:
            win.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append([player_pos[0] + player_size // 2 - 5, player_pos[1]])
                    if event.key == pygame.K_p:
                        is_paused = True
                    if event.key == pygame.K_b and bombs > 0:
                        enemies.clear()
                        bombs -= 1

            # Movimiento jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
                player_pos[0] += player_speed
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= player_speed
            if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
                player_pos[1] += player_speed

            # Movimiento enemigos
            for enemy in enemies[:]:
                enemy[1] += enemy_speed
                if detect_collision(player_pos, player_size, enemy, enemy_size):
                    print("¡Perdiste! Puntuación:", score)
                    running = False
                if enemy[1] >= HEIGHT:
                    enemies.remove(enemy)
                    enemies.append(spawn_enemy())
                    score += 1
                    if score % 5 == 0:
                        enemies.append(spawn_enemy())

            # Movimiento de balas
            for bullet in bullets[:]:
                bullet[1] -= bullet_speed
                if bullet[1] < 0:
                    bullets.remove(bullet)
                else:
                    for enemy in enemies[:]:
                        if detect_collision(bullet, 10, enemy, enemy_size):
                            enemies.remove(enemy)
                            bullets.remove(bullet)
                            enemies.append(spawn_enemy())
                            score += 5
                            if score >= 200 and bombs == 0:
                                bombs = 1
                            if score >= 300 and not upgrade:
                                upgrade = True
                                player_img = player_img_2
                            break

            # Dibujar jugador
            win.blit(player_img, (player_pos[0], player_pos[1]))

            # Dibujar enemigos
            for enemy in enemies:
                win.blit(enemy_img, (enemy[0], enemy[1]))

            # Dibujar balas
            for bullet in bullets:
                pygame.draw.rect(win, BLACK, (bullet[0], bullet[1], 10, 20))

            # Puntaje y bombas
            font = pygame.font.SysFont("Arial", 24)
            score_text = font.render(f"Puntuación: {score}", True, BLACK)
            win.blit(score_text, (10, 10))

            if bombs > 0:
                bomb_text = font.render("¡Bomba lista! Presiona B", True, (255, 0, 0))
                win.blit(bomb_text, (10, 40))

            pygame.display.update()
            clock.tick(30)

        else:
            # Pantalla de pausa
            font = pygame.font.SysFont("Arial", 40)
            text = font.render("Juego en pausa. Presiona P para continuar", True, BLACK)
            win.blit(text, (30, HEIGHT // 2 - 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    is_paused = False

def main_menu():
    menu = True
    while menu:
        win.fill(WHITE)
        font = pygame.font.SysFont("Arial", 40)
        text = font.render("Presiona una tecla y empieza a jugar", True, BLACK)
        win.blit(text, (50, HEIGHT // 2 - 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                menu = False

    game_loop()

main_menu()
