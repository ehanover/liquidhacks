import pygame
import navigator

class Enemy(pygame.sprite.Sprite):

    def move_to_target(self):
        if self.target is None or self.dead:
            return
        (a, b) = navigator.path_to(self, self.target)
        self.vx = a
        self.vy = b

    def move(self):
        if self.target is None or self.dead:
            return
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

    def __init__(self, x, y, img):
        super().__init__() # pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 5
        self.vx = None
        self.vy = None

        self.target = None
        self.dead = False
        self.health = 100
