from classes.maze_init import *

"""Code in this if block will only run if that module is the entry point of the program.
A while loop is created to ensure that the program continues until the player decides to stop or press echap.
We instantiate a game object, of the class Maze_init, which takes as parameter the name of the text file level_1.
"""

if __name__ == '__main__':

    while 1:
        game = Maze_init("level_1")
        if game.game_mov.combat.game_pursuit == False:
            break
