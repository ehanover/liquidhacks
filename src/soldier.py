from constants import *
import navigator
import pygame

class Soldier(pygame.sprite.Sprite):

    speed = 4.5
    # range = 100

    def set_target(self, t):
        if t is None:
            self.vx = 0.0
            self.vy = 0.0
        else:
            self.target = t
            (dx, dy) = navigator.path_to(self, self.target)
            self.vx = dx * Soldier.speed
            self.vy = dy * Soldier.speed

    def try_move(self, others):
        vxs = [self.vx, 0.7*self.vx - 0.7*self.vy, 0.7*self.vx + 0.7*self.vy]
        vys = [self.vy, 0.7*self.vx + 0.7*self.vy, -0.7*self.vx + 0.7*self.vy]
        for i in range(len(vxs)):
            self.rect.x += vxs[i]
            self.rect.y += vys[i]
            for other in others:
                if self.rect.colliderect(other):
                    self.rect.x -= vxs[i]
                    self.rect.y -= vys[i]
                else:
                    return

    def move(self, others):
        # self.rect.x += self.vx # TODO multiply by delta time?
        # self.rect.y += self.vy
        self.try_move(others)

    def __init__(self, x, y, img):
        super().__init__() # pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.target = None
        self.vx = 0.0
        self.vy = 0.0

        self.health = 100
        self.dead = False
        # self.selected = False
        self.target = None

    def displayHP(self, x, y):
        colorVal = self.health//100

        pass
    def changeColor(self, newColor):
        #self.image = pygame.image.fromstring(pygame.image.tostring(self.image, "RGBA"), self.image.get_size(), "RGBA")
        w, h = self.image.get_size()
        r, g, b = newColor
        for i in range(h):
            for j in range(w):
                oldColor = self.image.get_at((j, i))
                oR = oldColor[0]
                oG = oldColor[1]
                oB = oldColor[2]
                oR -= ((1 - (self.health/100))*(oR - r)//1)
                oG -= ((1 - (self.health/100))*(oG - g)//1)
                oB -= ((1 - (self.health/100))*(oB - b)//1)
                if (self.health < 0):
                    self.health = 0
                    break
                self.image.set_at((j, i), (oR,oG,oB))
        #self.image = new_image
                #print(self.health)
                #print(oR, oG,oB)
        # pygame.draw.rect(win, )
    '''
    def palette_swap(picture, oldColor, newColor):
        picTemp = pygame.Surface(health.img.get_size())
        picTemp.fill(newColor)
        picture.set_colorkey(oldColor)
        picTemp.blit(picture, (0,0))
        return picTemp



    def attack(self):
        if (checkAttack):
            pass


    def moveTo(self, toX, toY):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == rightClick:
            while (true):
                if x == toX and y == toY:
                    break
                if x < toX:
                    x += vel
                else:
                    x -= vel
                if y < toY:
                    y += vel
                else:
                    y -= vel

    def checkAttack(self, check):
        pass
    '''
