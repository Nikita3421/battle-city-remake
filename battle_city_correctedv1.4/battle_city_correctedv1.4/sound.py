import pygame
import time
import sys

pygame.init()
pygame.mixer.init() 

#screen = pygame.display.set_mode((800, 600))

#FPS = 60
clock = pygame.time.Clock()

# Все нужные звуковые еффекты здесь!!!

menu_music = 'sound/menu.mp3'
game_music = 'sound/battle_sound.mp3'
button_click_sound = pygame.mixer.Sound('sound/click.mp3')


shot_sound = pygame.mixer.Sound('sound/shoot.mp3')
hit_sound = pygame.mixer.Sound('sound/hit.wav')
miss_sound = pygame.mixer.Sound('sound/miss.wav')

movement_sound = pygame.mixer.Sound('sound/drive.mp3')
win_sound = pygame.mixer.Sound('sound/win.wav')
game_over_sound = pygame.mixer.Sound('sound/over.wav')

pygame.mixer.music.set_volume(0.5)

pygame.mixer.music.load(game_music)
pygame.mixer.music.play(-1)

# def play_sound(sound):
#     pygame.mixer.Sound.play(sound)

#pygame.mixer.music.play()  # Воспроизведение музыки
# time.sleep(1)
# # play_sound(hit_sound)

pygame.mixer.Sound.play(movement_sound) 

in_menu = True
in_game = False

while in_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Начало игры остановка музыки меню и запуск музыки игры
                pygame.mixer.music.stop()
                pygame.mixer.music.load(game_music)
                pygame.mixer.music.play(-1)
                in_game = True
                in_menu = False
                pygame.mixer.Sound.play(button_click_sound)

# Основной цикл игры
while in_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_game = False

# Завершение Pygame
# pygame.mixer.music.stop()
# pygame.quit()
# sys.exit()