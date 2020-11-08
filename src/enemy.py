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

    def move(self, others):
        clean_x = self.rect.x
        clean_y = self.rect.y
        vxs = [self.vx, 0.7*self.vx - 0.7*self.vy, 0.7*self.vx + 0.7*self.vy, 0.17*self.vx - 0.98*self.vy, 0.17*self.vx + 0.98*self.vy, -self.vy, self.vy]
        vys = [self.vy, 0.7*self.vy + 0.7*self.vy, -0.7*self.vx + 0.7*self.vy, 0.98*self.vx + 0.17*self.vy, -0.98*self.vx + 0.17*self.vy, self.vx, -self.vx]
        for i in range(len(vxs)):
            self.rect.x += vxs[i]
            self.rect.y += vys[i]
            if navigator.calc_collisions(self, others):
                self.rect.x = clean_x
                self.rect.y = clean_y
                continue
            else:
                return

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
