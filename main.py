import pygame
import random

from agent import Agent
from ui import *
from sound import *
from game_logic import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Runner")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Arial", 44, bold=True)
font_small = pygame.font.SysFont("Arial", 24)

LANE_WIDTH = WIDTH // 3
LANES_X = [
    LANE_WIDTH // 2 - PLAYER_SIZE // 2,
    WIDTH // 2 - PLAYER_SIZE // 2,
    (5 * LANE_WIDTH) // 2 - PLAYER_SIZE // 2
]

snow = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(40)]

flash_timer = 0
last_speed_level = 0

MENU, PLAYING, GAME_OVER = 0, 1, 2
state = MENU

player, obstacles, score, spawn_timer = reset_game(Agent, LANES_X, LANE_WIDTH, HEIGHT)
game_over_score = 0
running = True

while running:
    clock.tick(60)
    screen.fill((10, 15, 25))
    draw_snow(screen, snow)

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU and 120 < mx < 280 and 300 < my < 360:
                click_sound.play()
                player, obstacles, score, spawn_timer = reset_game(Agent, LANES_X, LANE_WIDTH, HEIGHT)
                state = PLAYING

            elif state == GAME_OVER and 120 < mx < 280 and 300 < my < 360:
                click_sound.play()
                player, obstacles, score, spawn_timer = reset_game(Agent, LANES_X, LANE_WIDTH, HEIGHT)
                state = PLAYING

    if state == PLAYING:
        current_speed = BASE_SPEED + (score // 200)

        spawn_timer += 1
        if spawn_timer > max(20, 45 - (score // 500)):
            spawn_timer = 0
            obstacles.append([random.choice(LANES_X), -OBSTACLE_SIZE])

        target_x = player.think(obstacles)

        if player.x < target_x:
            player.x = min(player.x + player.speed, target_x)
        elif player.x > target_x:
            player.x = max(player.x - player.speed, target_x)

        for ob in obstacles[:]:
            ob[1] += current_speed

            p_rect = pygame.Rect(player.x + 5, player.y + 5, PLAYER_SIZE - 10, PLAYER_SIZE - 10)
            o_rect = pygame.Rect(ob[0] + 5, ob[1] + 5, OBSTACLE_SIZE - 10, OBSTACLE_SIZE - 10)

            if p_rect.colliderect(o_rect):
                hit_sound.play()
                state = GAME_OVER
                game_over_score = score

            if ob[1] > HEIGHT:
                obstacles.remove(ob)
                score += 10
                score_sound.play()

    for lx in LANES_X:
        for y in range(0, HEIGHT, 20):
            pygame.draw.line(screen, (60, 60, 80), (lx + PLAYER_SIZE//2, y), (lx + PLAYER_SIZE//2, y+10), 2)

    pygame.draw.rect(screen, ACCENT, (player.x, player.y, PLAYER_SIZE, PLAYER_SIZE), border_radius=8)

    for ob in obstacles:
        pygame.draw.rect(screen, DANGER, (ob[0], ob[1], OBSTACLE_SIZE, OBSTACLE_SIZE), border_radius=6)

    screen.blit(font_small.render(str(score), True, WHITE), (10, 10))

    if state == MENU:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(font_big.render("LANE RUNNER", True, ACCENT), (WIDTH//2 - 100, 170))
        draw_button(screen, 120, 300, 160, 60, "START", font_small, 120 < mx < 280 and 300 < my < 360)

    elif state == GAME_OVER:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(140)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(font_big.render("GAME OVER", True, DANGER), (WIDTH//2 - 120, 150))
        screen.blit(font_small.render(f"SCORE: {game_over_score}", True, WHITE), (WIDTH//2 - 60, 220))

        draw_button(screen, 120, 300, 160, 60, "RESTART", font_small, 120 < mx < 280 and 300 < my < 360)

    if flash_timer > 0:
        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.set_alpha(40)
        flash.fill((200, 240, 255))
        screen.blit(flash, (0, 0))
        flash_timer -= 1

    pygame.display.flip()

pygame.quit()