import pygame
from pygame.locals import *
import button

pygame.init()

screen_width = 800
screen_height = 660

pygame.display.set_caption('Game Menu')

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

run = True
game_state = 'game'
menu_state = 'main'
GRAVITY = 1

pause_image = pygame.image.load('assets/button_pause.png').convert()
pause_image.set_colorkey((255, 255, 255))
continue_image = pygame.image.load('assets/button_continue.png').convert()
options_image = pygame.image.load('assets/button_options.png').convert()
quit_game_image = pygame.image.load('assets/button_quit_game.png').convert()
graphics_image = pygame.image.load('assets/button_graphics.png').convert()
audio_image = pygame.image.load('assets/button_audio.png').convert()
controls_image = pygame.image.load('assets/button_controls.png').convert()
quit_image = pygame.image.load('assets/button_quit.png').convert()

pause_button = button.Button(int(screen_width / 2 - pause_image.get_width() / 2), int(screen_height / 2 - pause_image.get_height() / 2), pause_image, 1)
continue_button = button.Button(int(screen_width / 2 - continue_image.get_width() / 2), 125, continue_image, 1)
options_button = button.Button(int(screen_width / 2 - options_image.get_width() / 2), 250, options_image, 1)
quit_game_button = button.Button(int(screen_width / 2 - quit_game_image.get_width() / 2), 375, quit_game_image, 1)
graphics_button = button.Button(int(screen_width / 2 - graphics_image.get_width() / 2), 75, graphics_image, 1)
audio_button = button.Button(int(screen_width / 2 - audio_image.get_width() / 2), 200, audio_image, 1)
controls_button = button.Button(int(screen_width / 2 - controls_image.get_width() / 2), 325, controls_image, 1)
quit_button = button.Button(int(screen_width / 2 - quit_image.get_width() / 2), 450, quit_image, 1)

while run:

    screen.fill((64, 0, 128))

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    if game_state == 'game':
        if pause_button.draw(screen):   
            game_state = 'paused'

    elif game_state == 'paused':
        if menu_state == 'main':
            if continue_button.draw(screen):  
                game_state = 'game'
            if options_button.draw(screen):
                menu_state = 'options'
            if quit_game_button.draw(screen):
                run = False
        elif menu_state == 'options':
            if graphics_button.draw(screen):
                print('GRAPHICS SETTING')
            if audio_button.draw(screen):
                print('AUDIO SETTINGS')
            if controls_button.draw(screen):
                print('CONTROLS SETTINGS')
            if quit_button.draw(screen):
                menu_state = 'main'

    clock.tick(60)
    pygame.display.update()

pygame.quit()
