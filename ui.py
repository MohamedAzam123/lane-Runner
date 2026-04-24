import pygame
import random

WIDTH, HEIGHT = 400, 600
PLAYER_SIZE = 40
OBSTACLE_SIZE = 50

ACCENT = (0, 255, 200)
DANGER = (255, 80, 80)
WHITE = (240, 240, 240)
ICE = (180, 220, 255)

def draw_snow(screen, snow):
    for s in snow:
        s[1] += s[2]
        if s[1] > HEIGHT:
            s[1] = 0
            s[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, ICE, (s[0], s[1]), 2)

def draw_button(screen, x, y, w, h, text, font, hover):
    color = ACCENT if hover else (30, 30, 50)
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=14)
    label = font.render(text, True, (0, 0, 0) if hover else WHITE)
    screen.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))