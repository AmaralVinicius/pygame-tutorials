import pygame
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
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

# Crosshair class
class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image, targets_group):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.gunshoot = pygame.mixer.Sound('assets/gunshoot.ogg')
        self.release = True
        self.targets_groups = targets_group

    def shoot(self):
        # Som e criação do tiro
        self.gunshoot.play()
        shots_group.add(Shot(shot_image, self.rect.center, self.targets_groups))

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
    def __init__(self, image, pos, targets_groups):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.created_time = pygame.time.get_ticks()
        self.targets_groups = targets_groups
        self.collisionable = True

    def update(self):
        self.current_time = pygame.time.get_ticks()

        # Identificação, colisão e exclusão do alvo
        if self.collisionable:
            for group in self.targets_groups:
                for target in pygame.sprite.spritecollide(self, group,False):
                    self.collisionable = False
                    target.kill()

        # Deleta tiro se após 10 segundos 
        if self.current_time - self.created_time >= 10000:
            self.kill()

# Gerar Alvos
def generate_targets(red_targets_group, green_targets_group, amount):
    # Limpa os grupos dos alvos
    red_targets_group.empty()
    green_targets_group.empty()

    # Gera alvos
    for i in range(1, amount + 1):
        if i % 2:
            red_targets_group.add(Target(red_target_image, (random.randint(0, screen_width - red_target_image.get_width()), random.randint(0, screen_height - red_target_image.get_height()))))
        else:
            green_targets_group.add(Target(green_target_image, (random.randint(0, screen_width - green_target_image.get_width()), random.randint(0, screen_height - green_target_image.get_height()))))

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
crosshair_group = pygame.sprite.GroupSingle(Crosshair(crosshair_image, (red_targets_group, green_targets_group)))

# Shot
shot_image = pygame.image.load('assets/shotmark.png').convert()
shot_image.set_colorkey((255, 255, 255))
shots_group = pygame.sprite.Group()

# Loop principal
while run:

    # Controle de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

    # Gera novos alvos e desativa colisão dos tiros restantes na tela
    if red_targets_group.__len__() == 0:
        for shot in shots_group:
            shot.collisionable = False
        generate_targets(red_targets_group, green_targets_group, 30)

    # Update da tela de jogo
    clock.tick(60)
    pygame.display.update()

pygame.quit() # Finalização geral
