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
    def __init__(self, image, target_group):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.gunshoot = pygame.mixer.Sound('assets/gunshoot.ogg')
        self.release = True
        self.crosshair_group = None
        self.target_group = target_group

    def shoot(self):
        self.gunshoot.play()
        shotmark_group.add(ShotMark(shotmark_image, self.rect.center))
        for target in pygame.sprite.groupcollide(self.target_group, self.crosshair_group,False, False):
            if target.rect.collidepoint(self.rect.center):
                target.kill()

    def update(self):
        self.crosshair_group = self.groups()[0]
        self.rect.center = pygame.mouse.get_pos()
        self.shooted = False

        if pygame.mouse.get_pressed()[0] and self.released:
            self.released = False
            self.shoot()

        if not pygame.mouse.get_pressed()[0]:
            self.released = True

# ShotMark class
class ShotMark(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.created_time = pygame.time.get_ticks()

    def update(self):
        self.current_time = pygame.time.get_ticks()

        if self.current_time - self.created_time >= 10000:
            self.kill()

# GameManager class
class GameManager():
    def __init__(self, red_targets_group, crosshair_group, shotmark_group):
        self.red_targets_group = red_targets_group
        self.crosshair_group = crosshair_group
        self.shotmark_group = shotmark_group
        
    def  run_game(self):

        if self.red_targets_group.__len__() == 0:
            for i in range(30):
                pos_x = random.randrange(0, screen_width - target_image.get_width())
                pos_y = random.randrange(0, screen_height - target_image.get_height())
                targets_group.add(Target(target_image, (pos_x, pos_y)))

        self.shotmark_group.update()
        self.shotmark_group.draw(screen)

        self.red_targets_group.update()
        self.red_targets_group.draw(screen)

        self.crosshair_group.update()
        self.crosshair_group.draw(screen)
    

# Targets
target_image = pygame.image.load('assets/target.png').convert()
target_image.set_colorkey((255, 255, 255))
targets_group = pygame.sprite.Group()
for i in range(30):
    pos_x = random.randrange(0, screen_width - target_image.get_width())
    pos_y = random.randrange(0, screen_height - target_image.get_height())
    targets_group.add(Target(target_image, (pos_x, pos_y)))

# Crosshair
crosshair_image = pygame.image.load('assets/mouse.png').convert()
crosshair_image.set_colorkey((0, 0, 0))
crosshair_group = pygame.sprite.GroupSingle(Crosshair(crosshair_image, targets_group))

# ShotMark
shotmark_image = pygame.image.load('assets/shotmark.png').convert()
shotmark_image.set_colorkey((255, 255, 255))
shotmark_group = pygame.sprite.Group()

# GameManager
game_manager = GameManager(targets_group, crosshair_group, shotmark_group)

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

    game_manager.run_game()

    # Update da tela de jogo
    clock.tick(60)
    pygame.display.update()

pygame.quit() # Finalização geral
