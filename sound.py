import pygame

pygame.mixer.init()

hit_sound = pygame.mixer.Sound("mixkit-alien-technology-button-3118.wav")
score_sound = pygame.mixer.Sound("mixkit-fantasy-game-success-notification-270.wav")
click_sound = pygame.mixer.Sound("mixkit-alien-technology-button-3118.wav")

hit_sound.set_volume(0.15)
score_sound.set_volume(0.25)
click_sound.set_volume(0.12)