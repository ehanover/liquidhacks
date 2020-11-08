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
        self.explosions = {}
        self.attacks = {}
        self.update_num = 0

        self.new_round(round_num)

    def make_soldiers(self, round_num):
        # Places the soldiers in a equidistant spiral
        num_soldiers = int((round_num + 5) * 1) # TODO tweak soldier formula to affect difficulty
        # num_soldiers = 1
        centerx = WIDTH//2
        centery = HEIGHT//2 + 120
        ret = []

        # Stolen from https://stackoverflow.com/a/13901170
        radius = 180
        chord = 2*SOLDIER_RADIUS # (how close each soldier is along the spiral)
        awayStep = radius/35 # (how tight the spiral is - lower val is looser)
        theta = chord / awayStep
        while len(ret) < num_soldiers:
            away = awayStep * theta # How far away from the center
            around = theta + 10 # How far around the center.
            ix = centerx + math.cos (around) * away # Convert 'around' and 'away' to X and Y.
            iy = centery + math.sin (around) * away
            ret.append(Soldier(ix, iy, self.soldier_img, self.soldier_selected_img))

            theta += chord / away # to a first approximation, the points are on a circle so the angle between them is chord/radius
        return ret

    def make_enemies(self, round_num):
        # Places the enemies in staggered rows at the top of the screen
        num_enemies = (round_num + 3) * 2 # TODO tweak enemy formula to affect difficulty
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
        for s in self.soldiers:
            s.kill()
        for e in self.enemies:
            e.kill()
        self.soldiers = self.make_soldiers(round_num)
        self.selected_soldiers = [0 for _ in range(len(self.soldiers))]
        self.enemies = self.make_enemies(round_num)
        self.deselect_all()
        for e in self.enemies:
            self.sprite_group.add(e)
        for s in self.soldiers:
            self.sprite_group.add(s)
        self.explosions = {}
        self.attacks = {}

    def update(self):
        assert(len(self.soldiers) == len(self.selected_soldiers))
        self.update_num = (self.update_num + 1) % FIRE_INTERVAL
        for e in self.enemies:
            detonating = False
            if e.dead:
                continue
            if e.health <= 0:
                e.dead = True
                detonating = True
            if e.target is None or e.target.dead:
                e.set_target(random.choice(self.soldiers))
                # e.set_target(navigator.closest_sprite(e, self.soldiers))
            else:  # recalculate vector
                e.set_target(e.target)
            if not e.dead:  # might have already exploded
                for s in self.soldiers:
                    if not s.dead and navigator.dist(e, s) < ENEMY_RADIUS:
                        e.dead = True
                        detonating = True
                        break
            if detonating:
                self.explosions[(e.rect.x, e.rect.y)] = 10
                for s in self.soldiers:
                    if navigator.dist(e, s) < DETONATE_DIST:
                        s.health -= DETONATE_DAMAGE
                        s.changeColor((255,0,0), (255, 255, 0))
            else:
                e.move(self.enemies)
        for e in self.enemies:
            if e.dead:
                e.kill()

        for i, s in enumerate(self.soldiers):
            if s.health <= 0:
                s.dead = True
                continue
            if s.dead:
                continue
            if s.target is not None:
                if navigator.dist(s, s.target) < PATHFIND_DIST:
                    s.set_target(None)
                    s.attacking = True
                else:
                    s.set_target(s.target)
            e = s.move(self.soldiers, self.enemies)
            if e is not None and self.update_num == 0:  # soldier is attacking
                e.health -= ATTACK_DAMAGE
                e.changeColor((255, 0, 0))
                self.attacks[((s.rect.x+SOLDIER_RADIUS//2, s.rect.y+SOLDIER_RADIUS//2), (e.rect.x+ENEMY_RADIUS//2, e.rect.y+ENEMY_RADIUS//2))] = 3

            if self.selected_soldiers[i]:
                self.soldiers[i].image = self.soldiers[i].selected_img
            else:
                self.soldiers[i].image = self.soldiers[i].img

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

        # explosions
        for pos, t in self.explosions.items():
            if t == 0:
                # remove?
                continue
            self.explosions[pos] -= 1
            s = pygame.Surface((DETONATE_DIST*2, DETONATE_DIST*2))
            s.fill((255, 255, 255))
            s.set_alpha(100)
            pygame.draw.circle(s, DETONATE_COLOR, (DETONATE_DIST, DETONATE_DIST), DETONATE_DIST)
            screen.blit(s, (pos[0] - DETONATE_DIST + ENEMY_RADIUS//2, pos[1] - DETONATE_DIST + ENEMY_RADIUS//2))

        poplist = []
        for (pos1, pos2), t in self.attacks.items():
            if t == 0:
                poplist.append((pos1, pos2))

        for key in poplist:
            self.attacks.pop(key)

        for (pos1, pos2), t in self.attacks.items():
            pygame.draw.line(screen, ATTACK_COLOR, pos1, pos2, ATTACK_WIDTH)
            self.attacks[(pos1, pos2)] -= 1

    def select(self, corner1, corner2):
        x_max = max(corner1[0], corner2[0])
        x_min = min(corner1[0], corner2[0])
        y_max = max(corner1[1], corner2[1])
        y_min = min(corner1[1], corner2[1])
        for i, s in enumerate(self.soldiers):
            center_x = s.rect.x + s.rect.width
            center_y = s.rect.y + s.rect.height
            if x_min <= center_x and center_x <= x_max and y_min <= center_y and center_y <= y_max:
                self.selected_soldiers[i] = True
            elif s.rect.contains(pygame.Rect(x_min, y_max, x_max - x_min, y_max - y_min)):
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
                s.attacking = False

    def attack_move(self, mouse_pos):
        # assert(len(self.soldiers) == len(self.selected_soldiers))
        for i, s in enumerate(self.soldiers):
            if self.selected_soldiers[i]:
                fake_sprite = navigator.FakeSprite()
                fake_sprite.rect.x = mouse_pos[0]
                fake_sprite.rect.y = mouse_pos[1]
                s.set_target(fake_sprite)
                s.attacking = True

    def stop(self):
        # assert(len(self.soldiers) == len(self.selected_soldiers))
        for i, s in enumerate(self.soldiers):
            if self.selected_soldiers[i]:
                s.set_target(None)
                s.attacking = True

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
