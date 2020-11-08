import math

def path_to(me, other):
        dx = other.rect.x - me.rect.x
        dy = other.rect.y - me.rect.y
        m = math.sqrt(dx*dx + dy*dy)
        return (dx/m, dy/m)

def dist(a, b):
    return math.sqrt( (a.rect.x-b.rect.x)**2 + (a.rect.y-b.rect.y)**2 )

def closest_sprite(me, sprites):
    maxdist = 100000000
    closest = sprites[0]
    for k in sprites:
        nd = dist(me, k)
        if nd < maxdist:
            maxdist = nd
            closest = k
    return closest

