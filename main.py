from classes.maze_init import *

if __name__ == '__main__':

    while 1:
        game = Maze_init("level_1")
        if game.game_mov.combat.game_pursuit == False:
            break
