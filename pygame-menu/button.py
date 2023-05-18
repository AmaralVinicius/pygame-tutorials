import pygame

class Button():
    def __init__(self, x, y, image, scale):
        size = (int(image.get_width() * scale), int(image.get_height() * scale))
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
        else:
            self.clicked = False

        if not pygame.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                action = True
        
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
