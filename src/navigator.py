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
        if m != 0:
            return (dx/m, dy/m)
        else:
            return (0, 0)

def dist(a, b):
    return math.sqrt( (a.rect.x+a.rect.width//2-b.rect.x-b.rect.width//2)**2 + (a.rect.y+a.rect.height//2-b.rect.y-b.rect.height//2)**2 )

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

