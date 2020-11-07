import pygame

class Entity:

    def __init__(self, img):
        self.img = img
        self.x = 60
        self.y = 90

    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,255), ((self.x, self.y), (30, 40)), 0)
