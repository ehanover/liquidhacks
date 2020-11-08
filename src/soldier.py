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

    def move(self):
        self.rect.x += self.vx # TODO multiply by delta time?
        self.rect.y += self.vy
        # print("x=" + str(self.rect.x) + ", vx=" + str(self.vx))

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

        keys = pygame.key.get_pressed()
        vel = 1
        leftClick = 1
        middleClick = 2
        rightClick = 3
        scrollUp = 4
        scrollDown = 5

    def displayHP(self, x, y):
        pass
        # pygame.draw.rect(win, )
    '''
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


