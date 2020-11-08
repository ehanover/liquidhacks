import pygame

class Soldier(pygame.sprite.Sprite):

    def __init__(self, x, y, img):
        super().__init__() # pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.dead = False
        self.selected = None

    def moveTo(self, x, y):
        pass
    def attack(self, range):
        pass
    def checkAttack(self, check):
        pass

