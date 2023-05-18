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
game_state = 'game' # Variável de estado principal do jogo
menu_state = 'main' # Variável de estado do menu

'''A quantidade de variáveis de estado em seu jogo irá variar de acordo com a necessidade.
Pense que todo estado do jogo (telas, menus, inventários, configurações) será controlado
dentro do loop do jogo utilizando este conceito de variáveis de estado.'''

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
continue_button = button.Button(int(screen_width / 2 - continue_image.get_width() / 2), 175, continue_image, 1.5)
options_button = button.Button(int(screen_width / 2 - options_image.get_width() / 2), 300, options_image, 1.5)
quit_game_button = button.Button(int(screen_width / 2 - quit_game_image.get_width() / 2), 425, quit_game_image, 1.5)
graphics_button = button.Button(int(screen_width / 2 - graphics_image.get_width() / 2), 135, graphics_image, 1.5)
audio_button = button.Button(int(screen_width / 2 - audio_image.get_width() / 2), 255, audio_image, 1.5)
controls_button = button.Button(int(screen_width / 2 - controls_image.get_width() / 2), 380, controls_image, 1.5)
quit_button = button.Button(int(screen_width / 2 - quit_image.get_width() / 2), 505, quit_image, 1.5)

while run:

    screen.fill((64, 0, 128))

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    # Conceito de variáveis de estado na prática
    # Estado do jogo
    if game_state == 'game':
        if pause_button.draw(screen):
            game_state = 'paused'
            ''''Utilização do retorno da classe de botões para alterar o estado do jogo.
            Mas lembre-se este é apenas um exemplo do conceito, qualquer condicional pode ser usada
            para alterar algum estado do jogo (botões do teclado, vida do player, outra variável de estado)'''

    elif game_state == 'paused':
        # Estado do menu (submenus, opções, créditos, etc.)
        if menu_state == 'main':
            if continue_button.draw(screen):  
                game_state = 'game'
            if options_button.draw(screen):
                menu_state = 'options' # Mudança de uma variável de estado
            if quit_game_button.draw(screen):
                run = False # Ação de fechar o jogo
        elif menu_state == 'options':
            if graphics_button.draw(screen):
                print('GRAPHICS SETTING') # Configurações
            if audio_button.draw(screen):
                print('AUDIO SETTINGS') 
            if controls_button.draw(screen):
                print('CONTROLS SETTINGS')
            if quit_button.draw(screen):
                menu_state = 'main'

    clock.tick(60)
    pygame.display.update()

pygame.quit()
