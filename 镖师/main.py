import pygame, sys
from scr.game import Game


def main():
    game = Game()
    game.run()
    pygame.display.quit()
    sys.exit()
if __name__ == '__main__':
    main()

