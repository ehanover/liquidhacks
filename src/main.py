import pygame
from constants import *
from state import State
import sys

def load_assets():
    assets_names = ["seahorse1.png", "stingray1.png"]
    assets_scales = [0.3, 0.42] # TODO move these values to constants.py
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
    amove_state = False
    box_select_state = False
    box_corner1 = (0, 0)

    while not game_over: # TODO create a menu screen
        # Update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    print("pressed a")
                    # toggle mouse cursor, toggle attack move
                    amove_state = not amove_state
                elif event.key == pygame.K_s:
                    print("pressed s")
                    # stop selected units
                    state.stop()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    pass
                elif event.key == pygame.K_s:
                    pass
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT:
                    print("pressed left click")
                    if amove_state:
                        # attack move
                        pass
                    else:
                        box_select_state = True
                        state.start_select()
                        box_corner1 = pygame.mouse.get_pos()
                elif event.button == MOUSE_RIGHT:
                    print("pressed right click")
                    # move

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_LEFT:
                    print("released left click")
                    if amove_state:
                        amove_state = False
                    elif box_select_state:
                        box_select_state = False
                        state.end_select()
                elif event.button == MOUSE_RIGHT:
                    print("released right click")

        if box_select_state:
            box_corner2 = pygame.mouse.get_pos()
            state.set_rectangle(box_corner1, box_corner2)

        # Draw
        state.draw(screen)

        # pygame.display.flip()
        pygame.display.update()

        state.update()

        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
