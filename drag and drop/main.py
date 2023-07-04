import pygame
from pygame.locals import *
from random import randint

# Inicialização geral
pygame.init()
clock = pygame.time.Clock()

# Tela de jogo
screen_width = 960
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Drag And Drop')

# Variáveis gerais
run = True

# Object class
class Object(pygame.sprite.Sprite):
    def __init__(self, size, pos, color):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hover = False
        self.clicked = False

    def update(self):
        # Estado de sobreposição do mouse sobre objeto (hover)
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0]:
            self.hover = True
        if self.hover and not self.rect.collidepoint(pygame.mouse.get_pos()):
            if not pygame.mouse.get_pressed()[0]:
                self.hover = False

        # Estado de click do mouse sobre objeto (clicked)
        if self.hover and pygame.mouse.get_pressed()[0]:
            if not self.clicked:
                self.clicked = True
                # Define a posição do click usando a diferença do centro do objeto, e da posição do mouse ao clicar
                self.point_clicked = (self.rect.centerx - pygame.mouse.get_pos()[0], self.rect.centery - pygame.mouse.get_pos()[1])
        else:
            self.clicked = False

        # Move o objeto com base na posição do click adicionando a posição do mouse, e a diferença calculada ao clicar
        if self.clicked:
            self.pos = (pygame.mouse.get_pos()[0] + self.point_clicked[0], pygame.mouse.get_pos()[1] + self.point_clicked[1])
            self.rect.center = self.pos

# Object gruop
objects_group = pygame.sprite.Group()
# Gera 10 objetos com posições e cores diferentes
for i in range(10):
    objects_group.add(Object((75, 75), (randint(0, 885), randint(0, 645)), (randint(0, 255), randint(0, 255), randint(0, 255))))

# Loop principal
while run:

    # Controle de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    # Background
    screen.fill((255, 255, 255))

    # Draw e Update dos objetos
    objects_group.update()
    objects_group.draw(screen)

    # Update da tela de jogo
    clock.tick(60)
    pygame.display.update()

pygame.quit() # Finalização geral
