import math
import pygame
from constants import *

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

def calc_collisions(me, others):
        for other in others:
            if other is not me and not other.dead:
                '''
                if me.rect.colliderect(other) != -1:
                    return True
                '''
                # tunable collision attempt
                max_x = max(me.rect.x, other.rect.x)
                min_x = min(me.rect.x, other.rect.x)
                max_y = max(me.rect.y, other.rect.y)
                min_y = min(me.rect.y, other.rect.y)
                if min_x + SOLDIER_RADIUS > max_x:
                    if min_y + SOLDIER_RADIUS > max_y:
                        return True
        return False

