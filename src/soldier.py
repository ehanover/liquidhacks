from constants import *
import navigator
import pygame
from constants import *

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

    def calc_collisions(self, others):
        for other in others:
            if other is not self and not other.dead:
                '''
                if self.rect.colliderect(other) != -1:
                    return True
                '''
                # tunable collision attempt
                max_x = max(self.rect.x, other.rect.x)
                min_x = min(self.rect.x, other.rect.x)
                max_y = max(self.rect.y, other.rect.y)
                min_y = min(self.rect.y, other.rect.y)
                if min_x + SOLDIER_RADIUS > max_x:
                    if min_y + SOLDIER_RADIUS > max_y:
                        return True
        return False


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


    def __init__(self, x, y, img, selected_img):
        super().__init__() # pygame.sprite.Sprite.__init__(self)

        self.img = img.copy()
        self.selected_img = selected_img.copy()
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # self.rect.width = SOLDIER_RADIUS
        # self.rect.height = SOLDIER_RADIUS

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
        # self.image = self.image.copy()
        w, h = self.img.get_size()

        r, g, b = newColor
        for i in range(h):
            for j in range(w):
                oldColor = self.img.get_at((j, i))
                oR = oldColor[0]
                oG = oldColor[1]
                oB = oldColor[2]

                oR -= ((1 - (self.health/100))*(oR - r)//1)
                oG -= ((1 - (self.health/100))*(oG - g)//1)
                oB -= ((1 - (self.health/100))*(oB - b)//1)
                if (self.health < 0):
                    self.health = 0
                    continue
                self.selected_img.set_at((j, i), (oR,oG,oB))
                self.img.set_at((j, i), (oR,oG,oB))
        self.img.set_colorkey((oR,oG,oB))
        self.selected_img.set_colorkey((oR,oG,oB))

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
