import pygame
from entity import Entity


def load_assets():
    assets_names = ["seahorse1.png"]
    assets_dict = {}
    for a in assets_names:
        assets_dict.update({a: pygame.image.load("assets/" + a)})
    return assets_dict

def main():
    # Init pygame
    pygame.init()
    FPS = 60
    WIDTH, HEIGHT = 64*10, 64*8
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Init assets
    assets_dict = load_assets()

    # Init game components
    player = Entity(assets_dict["seahorse1.png"])
    gameOver = False

    while not gameOver: # TODO create a menu screen
        # Update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("pressed left")
                if event.key == pygame.K_RIGHT:
                    print("pressed right")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("")

        # Draw
        screen.fill((255, 255, 255))

        player.draw(screen)
        # pygame.display.flip()
        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
