import pygame
import navigator

class Enemy(pygame.sprite.Sprite):

    speed = 3.1

    def set_target(self, t):
        self.target = t
        if self.target is None or self.dead:
            return
        (dx, dy) = navigator.path_to(self, self.target)
        self.vx = dx * Enemy.speed
        self.vy = dy * Enemy.speed

    def move(self):
        if self.target is None or self.dead:
            return
        if self.target.dead:
            self.target = None # the target will get resassigned by state.py
            self.vx = 0.0
            self.vy = 0.0
            return
        self.rect.x += self.vx  # TODO multiply by delta time?
        self.rect.y += self.vy

    def __init__(self, x, y, img):
        super().__init__() # pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vx = 0.0
        self.vy = 0.0

        self.target = None
        self.dead = False
        self.health = 100
