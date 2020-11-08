import pygame
import navigator

class Enemy(pygame.sprite.Sprite):

    speed = 2

    def set_target(self, t):
        self.target = t
        if self.target is None or self.dead:
            return
        (a, b) = navigator.path_to(self, self.target)
        self.vx = a
        self.vy = b

    def move(self):
        if self.target is None or self.dead:
            return
        if self.target.dead:
            self.target = None # the target will get resassigned by state.py
            self.vx = 0
            self.vy = 0
            return
        self.rect.x += self.vx * Enemy.speed
        self.rect.y += self.vy * Enemy.speed

    def __init__(self, x, y, img):
        super().__init__() # pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vx = 0
        self.vy = 0

        self.target = None
        self.dead = False
        self.health = 100
