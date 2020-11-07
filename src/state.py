import pygame
from enemy import Enemy
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
        self.new_round(round_num)

    def make_soldiers(self, round_num):
        return [Soldier(random.randrange(0, 200), random.randrange(0, 200), self.soldier_img) for _ in range(4)] # TODO update formula for difficulty

    def make_enemies(self, round_num):
        return [Enemy(random.randrange(0, 200), random.randrange(0, 200), self.enemy_img) for _ in range(10)] # TODO update formula for difficulty

    def new_round(self, round_num):
        self.deselect_all()
        self.soldiers = self.make_soldiers(round_num)
        self.enemies = self.make_enemies(round_num)
        for e in self.enemies:
            self.sprite_group.add(e)
        for s in self.soldiers:
            self.sprite_group.add(s)


    def draw(self, screen):
        screen.fill((255, 255, 255))
        # for s in self.soldiers:
        #     s.draw(screen)
        # for e in self.enemies:
        #     e.draw(screen)
        self.sprite_group.draw(screen)

    def select(self, corner1, corner2):
        x_max = max(corner1[0], corner2[0])
        x_min = min(corner1[0], corner2[0])
        y_max = max(corner1[1], corner2[1])
        y_min = min(corner1[1], corner2[1])
        for i, s in enumerate(soldiers):
            if x_min <= s.x and s.x <= x_max and y_min <= s.y and s.y <= y_max:
                selected_soldiers[i] = True
            else:
                selected_soldiers[i] = False
                
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
