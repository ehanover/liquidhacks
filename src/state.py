import pygame
from constants import *
from enemy import Enemy
import navigator
import math
import random
from soldier import Soldier

class State:
    def __init__(self, round_num, assets_dict):

        self.soldier_img = assets_dict["seahorse1.png"]
        self.soldier_selected_img = assets_dict["seahorse1_selected.png"]
        self.enemy_img = assets_dict["stingray1.png"]
        self.sprite_group = pygame.sprite.Group()
        self.soldiers =  []
        self.enemies = []
        self.selected_solders = []  # bool array
        self.selecting = False
        self.amoving = False
        self.corner1 = (0, 0)

        self.new_round(round_num)

    def make_soldiers(self, round_num):
        # Places the soldiers in a equidistant spiral
        num_soldiers = int((round_num + 30) * 0.8) # TODO tweak soldier formula to affect difficulty
        # num_soldiers = 1
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
        # num_enemies = 1
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
        assert(len(self.soldiers) == len(self.selected_soldiers))
        for e in self.enemies:
            if e.dead:
                continue
            if e.target is None:
                e.set_target(random.choice(self.soldiers))
                # e.set_target(navigator.closest_sprite(e, self.soldiers))
            else:  # recalculate vector
                e.set_target(e.target)
            for s in self.soldiers:
                if navigator.dist(e, s) < DETONATE_DIST:
                    s.health -= DETONATE_DAMAGE
                    e.dead = True
                    continue  # 1 or 2? doesnt matter rly
            e.move(self.enemies)
        for e in self.enemies:
            if e.dead:
                e.kill()

        for i, s in enumerate(self.soldiers):
            if s.dead:
                continue
            if s.health <= 0:
                s.dead = True
                continue
            if s.target is not None:
                if navigator.dist(s, s.target) < PATHFIND_DIST:
                    s.set_target(None)
                else:
                    s.set_target(s.target)
            s.move(self.soldiers)

            if self.selected_soldiers[i]:
                self.soldiers[i].image = self.soldier_selected_img
            else:
                self.soldiers[i].image = self.soldier_img

        for s in self.soldiers:
            if s.dead:
                s.kill()

        # self.enemies = [e for e in self.enemies if not e.dead]
        # self.soldiers = [s for s in self.soldiers if not s.dead]

    def draw(self, screen, mouse_pos):
        screen.fill((255, 255, 255))
        # for s in self.soldiers:
        #     s.draw(screen)
        # for e in self.enemies:
        #     e.draw(screen)
        self.sprite_group.draw(screen)
        

        # transparent stuff is copied from stackoverflow
        if self.amoving:
            s = pygame.Surface((SOLDIER_RADIUS, SOLDIER_RADIUS))
            s.set_alpha(100)
            s.fill((255, 255, 0))
            screen.blit(s, (mouse_pos[0] - SOLDIER_RADIUS / 2, mouse_pos[1] - SOLDIER_RADIUS / 2))

        elif self.selecting:
            left = min(self.corner1[0], mouse_pos[0])
            top = min(self.corner1[1], mouse_pos[1])
            width = abs(self.corner1[0] - mouse_pos[0])
            height = abs(self.corner1[1] - mouse_pos[1])
            s = pygame.Surface((width, height))
            s.set_alpha(100)
            s.fill(SELECT_COLOR)
            screen.blit(s, (left, top))

    def select(self, corner1, corner2):
        x_max = max(corner1[0], corner2[0])
        x_min = min(corner1[0], corner2[0])
        y_max = max(corner1[1], corner2[1])
        y_min = min(corner1[1], corner2[1])
        for i, s in enumerate(self.soldiers):
            if x_min <= s.rect.x and s.rect.x + SOLDIER_RADIUS <= x_max and y_min <= s.rect.y and s.rect.y + SOLDIER_RADIUS <= y_max:
                self.selected_soldiers[i] = True
            else:
                self.selected_soldiers[i] = False
                
    def select_all(self):
        self.selected_soldiers = [1 for _ in self.selected_soldiers]

    def deselect_all(self):
        self.selected_soldiers = [0 for _ in self.selected_soldiers]

    def move(self, mouse_pos):
        # assert(len(self.soldiers) == len(self.selected_soldiers))
        for i, s in enumerate(self.soldiers):
            if self.selected_soldiers[i]:
                fake_sprite = navigator.FakeSprite()
                fake_sprite.rect.x = mouse_pos[0]
                fake_sprite.rect.y = mouse_pos[1]
                s.set_target(fake_sprite)

    def attack_move(self, mouse_pos):
        # assert(len(self.soldiers) == len(self.selected_soldiers))
        for i, s in enumerate(self.soldiers):
            if self.selected_soldiers[i]:
                pass

    def stop(self):
        # assert(len(self.soldiers) == len(self.selected_soldiers))
        for i, s in enumerate(self.soldiers):
            if self.selected_soldiers[i]:
                pass

    def start_select(self, corner1):
        self.corner1 = corner1
        self.selecting = True

    def end_select(self, corner2):
        self.select(self.corner1, corner2)
        self.selecting = False

    def get_status(self):
        for s in self.soldiers:
            if not s.dead:
                for e in self.enemies:
                    if not e.dead:
                        return ROUND_IN_PROGRESS
                return ROUND_WIN
        return ROUND_LOSS
