import pygame
import random

pygame.mixer.init()

# sounds setup

hit_sound = pygame.mixer.Sound("mixkit-alien-technology-button-3118.wav")
score_sound = pygame.mixer.Sound("mixkit-fantasy-game-success-notification-270.wav")
click_sound = pygame.mixer.Sound("mixkit-alien-technology-button-3118.wav")

hit_sound.set_volume(0.15)
score_sound.set_volume(0.25)
click_sound.set_volume(0.12)

# lane globals

LANE_WIDTH = None
LANES_X = None

# AI agent class

class Agent:
    def __init__(self, lanes_x, lane_width, height):
        global LANE_WIDTH, LANES_X
        LANE_WIDTH = lane_width
        LANES_X = lanes_x
        self.x = LANES_X[1]
        self.y = height - 100
        self.speed = 10

    def calculate_utility(self, lane_x, obstacles):
        danger = 0
        for ob in obstacles:
            ox, oy = ob[0], ob[1]
            if abs(ox - lane_x) < LANE_WIDTH // 2 + 10:
                dist_y = self.y - oy
                if dist_y > 0:
                    danger += (100000 / (dist_y + 1))
        return 1000 - danger

    def think(self, obstacles):
        utilities = [self.calculate_utility(lx, obstacles) for lx in LANES_X]
        return LANES_X[utilities.index(max(utilities))]

# game setup

WIDTH, HEIGHT = 400, 600
PLAYER_SIZE = 40
OBSTACLE_SIZE = 50
BASE_SPEED = 4

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lane Runner")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Arial", 44, bold=True)
font_small = pygame.font.SysFont("Arial", 24)

# lanes positions

LANE_WIDTH = WIDTH // 3
LANES_X = [
    LANE_WIDTH // 2 - PLAYER_SIZE // 2,
    WIDTH // 2 - PLAYER_SIZE // 2,
    (5 * LANE_WIDTH) // 2 - PLAYER_SIZE // 2
]

# colors

ACCENT = (0, 255, 200)
DANGER = (255, 80, 80)
WHITE = (240, 240, 240)
ICE = (180, 220, 255)

# snow particles

snow = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(40)]

flash_timer = 0
last_speed_level = 0

MENU, PLAYING, GAME_OVER = 0, 1, 2
state = MENU

# draw snow

def draw_snow():
    for s in snow:
        s[1] += s[2]
        if s[1] > HEIGHT:
            s[1] = 0
            s[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, ICE, (s[0], s[1]), 2)

# draw button

def draw_button(x, y, w, h, text, font, hover=False):
    color = ACCENT if hover else (30, 30, 50)
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=14)
    label = font.render(text, True, (0, 0, 0) if hover else WHITE)
    screen.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))

# reset game

def reset_game():
    player = Agent(LANES_X, LANE_WIDTH, HEIGHT)
    obstacles = []
    score = 0
    spawn_timer = 0
    return player, obstacles, score, spawn_timer

player, obstacles, score, spawn_timer = reset_game()
game_over_score = 0
running = True

# main loop

while running:
    clock.tick(60)
    screen.fill((10, 15, 25))
    draw_snow()

    mx, my = pygame.mouse.get_pos()

    # events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU and 120 < mx < 280 and 300 < my < 360:
                click_sound.play()
                player, obstacles, score, spawn_timer = reset_game()
                state = PLAYING

            elif state == GAME_OVER and 120 < mx < 280 and 300 < my < 360:
                click_sound.play()
                player, obstacles, score, spawn_timer = reset_game()
                state = PLAYING

    # gameplay

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

    # draw lanes

    for lx in LANES_X:
        for y in range(0, HEIGHT, 20):
            pygame.draw.line(screen, (60, 60, 80), (lx + PLAYER_SIZE//2, y), (lx + PLAYER_SIZE//2, y+10), 2)

    # draw player

    pygame.draw.rect(screen, ACCENT, (player.x, player.y, PLAYER_SIZE, PLAYER_SIZE), border_radius=8)

    # draw obstacles

    for ob in obstacles:
        pygame.draw.rect(screen, DANGER, (ob[0], ob[1], OBSTACLE_SIZE, OBSTACLE_SIZE), border_radius=6)

    screen.blit(font_small.render(str(score), True, WHITE), (10, 10))

    # menu

    if state == MENU:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(font_big.render("LANE RUNNER", True, ACCENT), (WIDTH//2 - 100, 170))
        draw_button(120, 300, 160, 60, "START", font_small, 120 < mx < 280 and 300 < my < 360)

    # game over

    elif state == GAME_OVER:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(140)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(font_big.render("GAME OVER", True, DANGER), (WIDTH//2 - 120, 150))
        screen.blit(font_small.render(f"SCORE: {game_over_score}", True, WHITE), (WIDTH//2 - 60, 220))

        draw_button(120, 300, 160, 60, "RESTART", font_small, 120 < mx < 280 and 300 < my < 360)

    if flash_timer > 0:
        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.set_alpha(40)
        flash.fill((200, 240, 255))
        screen.blit(flash, (0, 0))
        flash_timer -= 1

    pygame.display.flip()

pygame.quit()