import math
import pygame

class FakeSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.dead = False


def path_to(me, other):
        dx = float(other.rect.x - me.rect.x)
        dy = float(other.rect.y - me.rect.y)
        m = math.sqrt(dx*dx + dy*dy)
        # print("dx:" + str(dx) + ", m=" + str(m))
        return (dx/m, dy/m)

def dist(a, b):
    return math.sqrt( (a.rect.x-b.rect.x)**2 + (a.rect.y-b.rect.y)**2 )

def closest_sprite(me, others):
    maxdist = 100000000
    closest = None
    for k in others:
        if k.dead:
            continue
        nd = dist(me, k)
        if nd < maxdist:
            maxdist = nd
            closest = k
    return closest

