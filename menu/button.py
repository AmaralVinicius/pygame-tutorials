import pygame

class Button():
    def __init__(self, x, y, image, scale = 1):
        pre_rect = image.get_rect()
        pre_rect.topleft = (x, y)
        # Variável pre_rect serve como uma memória da posição e tamanho da imagem antes de escalar caso um valor scale seja passado
        size = (int(image.get_width() * scale), int(image.get_height() * scale))
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.center = pre_rect.center
        #Uso o retangulo pre_rect para deixar o botão  sempre centralizado de acordo com o tamanho e posição original
        self.clicked = False
        '''A forma que você ira posicionar os seus botões vai sempre depender
        da  forma como você desenvolve seus menus, botões e etc.
        mas a base sempre será rects (pygame.Rect), o que é bastante versátil'''

    def draw(self, surface):
        # Função principal que desenha o botão e retorna se foi clicado ou não
        action = False
        pos = pygame.mouse.get_pos() # Posição do mouse

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
        else:
            self.clicked = False

        if not pygame.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                action = True
                '''Irá retonar True apenas se o mouse (botão direito) for solto e o mouse estiver sobre o botão
                self.click é uma variável controle para que só seja retornada a ação de fato sobre condições mais controláveis'''
        
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
