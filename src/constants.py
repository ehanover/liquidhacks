import pygame

WIDTH = 1280
HEIGHT = 900

FPS = 30

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3

ENEMY_RADIUS = 42  # hardcoded to be the same as e.rect.x and e.rect.y
SOLDIER_RADIUS = 30

ENEMY_SPEED = 4.4
SOLDIER_SPEED = 4.5

SOLDIER_RANGE = 110
ATTACK_DAMAGE = 15
ATTACK_WIDTH = 2
FIRE_INTERVAL = 5

PATHFIND_DIST = 10
DETONATE_DIST = 2*max(ENEMY_RADIUS, SOLDIER_RADIUS)
DETONATE_DAMAGE = 51

SELECT_COLOR = pygame.Color(50, 255, 250)
DETONATE_COLOR = pygame.Color(0, 50, 255)
ATTACK_COLOR = pygame.Color(255, 0, 255)

ROUND_WIN = 0
ROUND_LOSS = 1
ROUND_IN_PROGRESS = 2