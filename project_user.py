import pygame
import random

pygame.init()
pygame.mixer.init()

# ==============================
# 🔊 SOUND
# ==============================
hit_sound = pygame.mixer.Sound("mixkit-alien-technology-button-3118.wav")
score_sound = pygame.mixer.Sound("mixkit-fantasy-game-success-notification-270.wav")
click_sound = pygame.mixer.Sound("mixkit-alien-technology-button-3118.wav")

hit_sound.set_volume(0.15)
score_sound.set_volume(0.10)
click_sound.set_volume(0.12)

# ==============================
# 🎮 SETUP
# ==============================
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
OBSTACLE_SIZE = 50
BASE_SPEED = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 LANE RUNNER PRO MAX")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Arial", 44, bold=True)
font_small = pygame.font.SysFont("Arial", 24)

LANE_WIDTH = WIDTH // 3
LANES_X = [
    LANE_WIDTH // 2 - PLAYER_SIZE // 2,
    WIDTH // 2 - PLAYER_SIZE // 2,
    (5 * LANE_WIDTH) // 2 - PLAYER_SIZE // 2
]

# ==============================
# 🎨 COLORS
# ==============================
ACCENT = (0, 255, 180)
DANGER = (255, 60, 60)
WHITE = (240, 240, 240)
BG_TOP = (5, 5, 20)
BG_BOTTOM = (20, 20, 40)

# ==============================
# 🔘 BUTTON
# ==============================
def draw_button(x, y, w, h, text, font, hover=False):
    if hover:
        pygame.draw.rect(screen, ACCENT,
                         (x-4, y-4, w+8, h+8), border_radius=16)

    pygame.draw.rect(screen, (20, 20, 40),
                     (x, y, w, h), border_radius=14)

    label = font.render(text, True, ACCENT)
    screen.blit(label, (
        x + w//2 - label.get_width()//2,
        y + h//2 - label.get_height()//2
    ))

# ==============================
# 🔁 RESET
# ==============================
def reset_game():
    return LANES_X[1], 1, [], 0, 0, BASE_SPEED, 1, 0

# ==============================
# 🎮 STATES
# ==============================
MENU, PLAYING, GAME_OVER = 0, 1, 2

state = MENU
player_x, player_lane, obstacles, score, spawn_timer, current_speed, level, speed_flash = reset_game()
game_over_score = 0

# ==============================
# 🎮 LOOP
# ==============================
running = True
while running:
    clock.tick(60)

    # 🎨 Gradient Background
    for y in range(HEIGHT):
        color = (
            BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * y // HEIGHT,
            BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * y // HEIGHT,
            BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * y // HEIGHT
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state in [MENU, GAME_OVER]:
                if 120 < mx < 280 and 300 < my < 360:
                    click_sound.play()
                    player_x, player_lane, obstacles, score, spawn_timer, current_speed, level, speed_flash = reset_game()
                    state = PLAYING

        if event.type == pygame.KEYDOWN and state == PLAYING:
            if event.key == pygame.K_LEFT and player_lane > 0:
                player_lane -= 1
            if event.key == pygame.K_RIGHT and player_lane < 2:
                player_lane += 1

    # ==============================
    # 🎮 GAME LOGIC
    # ==============================
    if state == PLAYING:

        # 🎯 Level System
        new_level = score // 200 + 1
        if new_level > level:
            level = new_level
            speed_flash = 10  # flash effect

        # 🚀 Smooth Speed Increase
        target_speed = BASE_SPEED + (level * 0.8)
        current_speed += (target_speed - current_speed) * 0.05
        current_speed = min(current_speed, 15)

        spawn_timer += 1
        if spawn_timer > max(15, 45 - int(level * 3)):
            spawn_timer = 0
            obstacles.append([random.choice(LANES_X), -OBSTACLE_SIZE])

        target_x = LANES_X[player_lane]

        if player_x < target_x:
            player_x += 8
        elif player_x > target_x:
            player_x -= 8

        for ob in obstacles[:]:
            ob[1] += current_speed

            p_rect = pygame.Rect(player_x + 5, HEIGHT - 100 + 5, PLAYER_SIZE - 10, PLAYER_SIZE - 10)
            o_rect = pygame.Rect(ob[0] + 5, ob[1] + 5, OBSTACLE_SIZE - 10, OBSTACLE_SIZE - 10)

            if p_rect.colliderect(o_rect):
                hit_sound.play()
                state = GAME_OVER
                game_over_score = score

            if ob[1] > HEIGHT:
                obstacles.remove(ob)
                score += 10
                score_sound.play()

    # ==============================
    # ⚡ SPEED FLASH EFFECT
    # ==============================
    if speed_flash > 0:
        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.set_alpha(40)
        flash.fill((0, 255, 200))
        screen.blit(flash, (0, 0))
        speed_flash -= 1

    # ==============================
    # 🛣️ ROAD MOTION
    # ==============================
    offset = pygame.time.get_ticks() // 5 % 20

    for lx in LANES_X:
        for y in range(-20, HEIGHT, 20):
            pygame.draw.line(screen, (80, 80, 120),
                             (lx + PLAYER_SIZE//2, y + offset),
                             (lx + PLAYER_SIZE//2, y + 10 + offset), 3)

    # ==============================
    # 🚗 PLAYER
    # ==============================
    for i in range(5):
        pygame.draw.rect(screen, (0, 255, 200),
                         (player_x - i, HEIGHT - 100 - i,
                          PLAYER_SIZE + i*2, PLAYER_SIZE + i*2),
                         border_radius=10)

    pygame.draw.rect(screen, ACCENT,
                     (player_x, HEIGHT - 100, PLAYER_SIZE, PLAYER_SIZE),
                     border_radius=10)

    # ==============================
    # 🚧 OBSTACLES
    # ==============================
    for ob in obstacles:
        pulse = (pygame.time.get_ticks() // 200) % 2
        color = (255, 80 + pulse*40, 80)

        pygame.draw.rect(screen, color,
                         (ob[0], ob[1], OBSTACLE_SIZE, OBSTACLE_SIZE),
                         border_radius=8)

    # ==============================
    # 💥 SCORE + LEVEL
    # ==============================
    screen.blit(font_small.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font_small.render(f"Level: {level}", True, ACCENT), (10, 40))

    # ==============================
    # 🎮 UI
    # ==============================
    if state == MENU:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(120)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

        title = font_big.render("LANE RUNNER", True, ACCENT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 170))

        draw_button(120, 300, 160, 60, "START", font_small, 120 < mx < 280 and 300 < my < 360)

    elif state == GAME_OVER:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(140)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

        title = font_big.render("GAME OVER", True, DANGER)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        txt = font_small.render(f"SCORE: {game_over_score}", True, WHITE)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 220))

        draw_button(120, 300, 160, 60, "RESTART", font_small, 120 < mx < 280 and 300 < my < 360)

    pygame.display.flip()

pygame.quit()