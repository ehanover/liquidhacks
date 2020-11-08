import pygame

class Soldier(pygame.sprite.Sprite):

    range = 100

    def __init__(self, x, y, img):
        super().__init__() # pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 5

        self.dead = False
        self.selected = None
        self.target = None
        keys = pygame.key.get_pressed()

    def attack(self):
        pass


    def moveTo(self, x, y):
        # if keys[pygame.K_RightCLick]
        pass
    
    def checkAttack(self, check):
        pass

