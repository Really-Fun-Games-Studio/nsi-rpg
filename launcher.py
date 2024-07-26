import sys
import src.main

if __name__ == '__main__':
    game = src.main.Game()
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == "debug":
            game.DEBUG_MODE = True
    game.loop()
