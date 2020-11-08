import pygame
from constants import *
from enemy import Enemy
import navigator
import math
import random
from soldier import Soldier

class State:
    def __init__(self, round_num, soldier_img, enemy_img):

        self.soldier_img = soldier_img
        self.enemy_img = enemy_img
        self.sprite_group = pygame.sprite.Group()
        self.soldiers =  []
        self.enemies = []
        self.selected_solders = []  # bool array
        self.selecting = False
        self.rectangle = ((0, 0), (0, 0))

        self.new_round(round_num)

    def make_soldiers(self, round_num):
        # Places the soldiers in a equidistant spiral
        num_soldiers = int((round_num + 30) * 0.8) # TODO tweak soldier formula to affect difficulty
        centerx = WIDTH//2
        centery = HEIGHT//2 + 120
        ret = []
        
        # Stolen from https://stackoverflow.com/a/13901170
        radius = 180
        chord = SOLDIER_RADIUS # (how close each soldier is along the spiral)
        awayStep = radius/35 # (how tight the spiral is - lower val is looser)
        theta = chord / awayStep
        while len(ret) < num_soldiers:
            away = awayStep * theta # How far away from the center
            around = theta + 10 # How far around the center.
            ix = centerx + math.cos (around) * away # Convert 'around' and 'away' to X and Y.
            iy = centery + math.sin (around) * away
            ret.append(Soldier(ix, iy, self.soldier_img))

            theta += chord / away # to a first approximation, the points are on a circle so the angle between them is chord/radius
        return ret

    def make_enemies(self, round_num):
        # Places the enemies in staggered rows at the top of the screen
        num_enemies = (round_num + 1) * 6 # TODO tweak enemy formula to affect difficulty
        num_cols = 10
        ret = []
        x = 0
        y = 0
        while len(ret) < num_enemies:
            ix = int( (WIDTH//2) + ((x - num_cols/2 + (y%2)/2) * ENEMY_RADIUS) )
            iy = int( (y + 1) * ENEMY_RADIUS )
            ret.append(Enemy(ix, iy, self.enemy_img))

            x += 1
            if(x >= num_cols):
                x = 0
                y += 1
        return ret

    def new_round(self, round_num):
        self.soldiers = self.make_soldiers(round_num)
        self.selected_soldiers = [0 for _ in range(len(self.soldiers))]
        self.enemies = self.make_enemies(round_num)
        self.deselect_all()
        for e in self.enemies:
            self.sprite_group.add(e)
        for s in self.soldiers:
            self.sprite_group.add(s)

    def update(self):
        for e in self.enemies:
            if e.target is None:
                e.set_target(navigator.closest_sprite(e, self.soldiers))
            elif navigator.dist(e, e.target) < DETONATE_DIST:
                e.dead = True
                continue
            e.move()
        for e in self.enemies:
            if e.dead:
                e.kill()


    def draw(self, screen):
        screen.fill((255, 255, 255))
        # for s in self.soldiers:
        #     s.draw(screen)
        # for e in self.enemies:
        #     e.draw(screen)
        self.sprite_group.draw(screen)

        if self.selecting:
            left = min(self.rectangle[0][0], self.rectangle[1][0])
            top = max(self.rectangle[0][1], self.rectangle[1][1])
            width = abs(self.rectangle[0][0] - self.rectangle[1][0])
            height = abs(self.rectangle[0][1] - self.rectangle[1][1])
            pygame.draw.rect(screen, SELECT_COLOR, pygame.Rect(left, top, width, height))

    def select(self, corner1, corner2):
        x_max = max(corner1[0], corner2[0])
        x_min = min(corner1[0], corner2[0])
        y_max = max(corner1[1], corner2[1])
        y_min = min(corner1[1], corner2[1])
        for i, s in enumerate(self.soldiers):
            if x_min <= s.rect.x and s.rect.x <= x_max and y_min <= s.rect.y and s.rect.y <= y_max:
                self.selected_soldiers[i] = True
            else:
                self.selected_soldiers[i] = False
                
    def select_all(self):
        self.selected_soldiers = [1 for _ in self.soldiers]

    def deselect_all(self):
        self.selected_soldiers = [0 for _ in self.soldiers]

    def move(self, mouse_pos):
        assert(len(self.soldiers) == len(self.selected_soldiers))
        pass

    def attack_move(self, mouse_pos):
        assert(len(self.soldiers) == len(self.selected_soldiers))
        pass

    def stop(self):
        assert(len(self.soldiers) == len(self.selected_soldiers))
        for i, s in enumerate(self.soldiers):
            if self.selected_soldiers[i]:
                pass

    def start_select(self):
        self.selecting = True

    def end_select(self):
        self.select(self.rectangle[0], self.rectangle[1])
        self.selecting = False

    def set_rectangle(self, corner1, corner2):
        self.rectangle = (corner1, corner2)