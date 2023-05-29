import pygame
from pygame.locals import *
import random

# Inicialização geral
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
clock = pygame.time.Clock()

# Tela de jogo
screen_width = 960
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shooter')
pygame.mouse.set_visible(False)

# Variáveis gerais
run = True
background = pygame.image.load('assets/background.png').convert()

# Target class
class Target(pygame.sprite.Sprite):
    def __init__(self, image, pos, value):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.value = value

# Crosshair class
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.gunshoot = pygame.mixer.Sound('assets/gunshoot.ogg')
        self.release = True

    def shoot(self):
        # Som e criação do tiro
        self.gunshoot.play()
        shots_group.add(Shot(shot_image, self.rect.center))

    def update(self):
        # Controle de criação de tiros com cliques únicos do mouse
        self.crosshair_group = self.groups()[0]
        self.rect.center = pygame.mouse.get_pos()
        self.shooted = False

        if pygame.mouse.get_pressed()[0] and self.released:
            self.released = False
            self.shoot()

        if not pygame.mouse.get_pressed()[0]:
            self.released = True

# Shot class
class Shot(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.created_time = pygame.time.get_ticks()
        self.collisionable = True
        self.targets_groups = (red_targets_group, green_targets_group)
        self.scorer_group = scorer_group

    def update(self):
        self.current_time = pygame.time.get_ticks()

        # Identificação, colisão e exclusão do alvo
        if self.collisionable:
            for group in self.targets_groups:
                for target in pygame.sprite.spritecollide(self, group,False):
                    self.collisionable = False # Desativa colisão do tiro, para não colidir com alvos novos caso sejam gerados
                    self.scorer_group.sprites()[0].change_score(target.value) # Envia o valor do alvo para o score
                    target.kill() # Deleta o alvo atingido

        # Deleta tiro se após 10 segundos 
        if self.current_time - self.created_time >= 10000:
            self.kill()

# Scorer class
class Scorer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("freesansbold", 125)
        self.score = 0
        self.last_score = 0
        self.color = (255, 255, 255)

    def change_score(self, value):
        self.last_score = self.score
        self.score += value

        # O score será vermelho sempre que menor que 1
        if self.score < 1:
            self.color = (255, 0, 0)
        else:
            # O score será vermelho se o jogador tiver a pontuação diminuída (Acertou o alvo errado, com value negativo)
            if self.last_score > self.score:
                self.color = (255, 0, 0)
            # O score será verde se o jogador tiver a pontuação aumentada (Acertou o alvo certo, com value positivo)
            if self.last_score < self.score:
                self.color = (0, 255, 0)

    def update(self):
        # Atualiza o score (a imagem) e a posição (o rect)
        self.image, self.rect = text(self.font, self.color, str(self.score))
        self.rect.center = (screen_width / 2, self.image.get_height())

# Gerar texto e seu rect correspondente
def text(font, color, text):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    return text_surface, text_rect

# Gerar Alvos
def generate_targets(red_targets_group, green_targets_group, amount):
    # Limpa os grupos dos alvos
    red_targets_group.empty()
    green_targets_group.empty()

    # Gera alvos
    for i in range(1, amount + 1):
        if i % 2:
            red_targets_group.add(Target(red_target_image, (random.randint(0, screen_width - red_target_image.get_width()), random.randint(0, screen_height - red_target_image.get_height())), +1))
        else:
            green_targets_group.add(Target(green_target_image, (random.randint(0, screen_width - green_target_image.get_width()), random.randint(0, screen_height - green_target_image.get_height())), -1))

# Red Targets
red_target_image = pygame.image.load('assets/red_target.png').convert()
red_target_image.set_colorkey((255, 255, 255))
red_targets_group = pygame.sprite.Group()

# Green Targets
green_target_image = pygame.image.load('assets/green_target.png').convert()
green_target_image.set_colorkey((255, 255, 255))
green_targets_group = pygame.sprite.Group()

# Crosshair
crosshair_image = pygame.image.load('assets/mouse.png').convert()
crosshair_image.set_colorkey((0, 0, 0))
crosshair_group = pygame.sprite.GroupSingle(Crosshair(crosshair_image))

# Shot
shot_image = pygame.image.load('assets/shotmark.png').convert()
shot_image.set_colorkey((255, 255, 255))
shots_group = pygame.sprite.Group()

# Scorer
scorer_group = pygame.sprite.GroupSingle(Scorer())

# Loop principal
while run:

    # Controle de eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    # Background
    for width in range(int(screen_width / background.get_width() + 1)):
        for height in range(int(screen_height / background.get_height() + 1)):
            screen.blit(background, (background.get_width() * width, background.get_height() * height))

    # Draw e Update dos grupos
    shots_group.update()
    shots_group.draw(screen)

    red_targets_group.draw(screen)
    green_targets_group.draw(screen)

    crosshair_group.update()
    crosshair_group.draw(screen)

    scorer_group.update()
    scorer_group.draw(screen)

    # Gera novos alvos e desativa colisão dos tiros restantes na tela
    if red_targets_group.__len__() == 0:
        for shot in shots_group:
            shot.collisionable = False
        generate_targets(red_targets_group, green_targets_group, 30)

    # Update da tela de jogo
    clock.tick(60)
    pygame.display.update()

pygame.quit() # Finalização geral
