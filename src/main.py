import pygame
from constants import *
from state import State
import sys

def load_assets():
    assets_names = ["seahorse1.png", "seahorse1_selected.png", "stingray1.png"]
    assets_scales = [0.45, 0.45, 0.42] # TODO move these values to constants.py
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
    font = pygame.font.SysFont(None, 24)

    game_over = False
    round_num = 0

    # Init game components
    # state holds all the state on the soldiers and the enemies
    # main holds all the state on the mouse and keyboard
    state = State(round_num, assets_dict)
    amove_state = False
    box_select_state = False

    while not game_over: # TODO create a menu screen

        if state.get_status() != ROUND_IN_PROGRESS:
            if state.get_status() == ROUND_WIN:
                pygame.time.wait(2000)
                round_num += 1
                state.new_round(round_num)
            else:
                pygame.time.wait(2000)
                game_over = True
                break

        # Update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    # print("pressed a")
                    # toggle mouse cursor, toggle attack move
                    amove_state = not amove_state
                    state.amoving = amove_state
                elif event.key == pygame.K_s:
                    # print("pressed s")
                    # stop selected units
                    state.stop()
                elif event.key == pygame.K_LCTRL:
                    state.select_all()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    pass
                elif event.key == pygame.K_s:
                    pass
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT:
                    # print("pressed left click")
                    if amove_state:
                        amove_state = False
                        state.amoving = False
                        state.attack_move(pygame.mouse.get_pos())
                    else:
                        box_select_state = True
                        state.start_select(pygame.mouse.get_pos())
                elif event.button == MOUSE_RIGHT:
                    # print("pressed right click")
                    if not amove_state:
                        state.move(pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_LEFT:
                    # print("released left click")
                    if box_select_state:
                        box_select_state = False
                        state.end_select(pygame.mouse.get_pos())
                elif event.button == MOUSE_RIGHT:
                    # print("released right click")
                    pass

        # Draw
        state.draw(screen, pygame.mouse.get_pos())

        img = font.render("Currently playing round " + str(1 + round_num), True, (50, 200, 200))
        screen.blit(img, (20, 20))

        # pygame.display.flip()
        pygame.display.update()

        state.update()

        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
