import pygame
from constants import *
from state import State
import sys

def load_assets():
    assets_names = ["seahorse1.png", "stingray1.png"]
    assets_scales = [0.8, 0.5]
    assets_dict = {}
    for n, s in zip(assets_names, assets_scales):
        img = pygame.image.load("assets/" + n)
        r = img.get_rect()
        img = pygame.transform.scale(img, (int(r[2]*s), int(r[3]*s)) )
        assets_dict.update({n: img})
    return assets_dict

assets_dict = load_assets()

def main():
    # Init pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    game_over = False
    round_num = 0

    # Init game components
    # state holds all the state on the soldiers and the enemies
    # main holds all the state on the mouse and keyboard
    state = State(round_num, assets_dict["seahorse1.png"], assets_dict["stingray1.png"])
    mouse_state = (pygame.MOUSEBUTTONUP, MOUSE_LEFT)
    key_state = (pygame.KEYUP, pygame.K_s)

    while not game_over: # TODO create a menu screen
        # Update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_state = (event.type, event.key)
                if event.key == pygame.K_a:
                    # toggle mouse cursor, toggle attack move
                    print("pressed a")
                elif event.key == pygame.K_s:
                    # stop selected units
                    print("pressed s")
                    state.stop()
                elif event.key == pygame.KMOD_CTRL:
                    # prep select all
                    print("pressed ctrl")
            
            elif event.type == pygame.KEYUP:
                key_state = (event.type, event.key)
                if event.key == pygame.KMOD_CTRL:
                    # stop prepping ctrl
                    print("released ctrl")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_state = (event.type, event.button)
                if event.button == MOUSE_LEFT:
                    # select or attack move
                    # if keystate()
                    print("pressed left click")
                elif event.button == MOUSE_RIGHT:
                    # move
                    print("pressed right click")
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_LEFT:
                    # release selection box
                    print("released left click")
                elif event.button == MOUSE_RIGHT:
                    print("released right click")

        # Draw
        state.draw(screen)

        # pygame.display.flip()
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
