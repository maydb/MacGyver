from definitions import *

if __name__ == '__main__':


    pos_hero = [1, 1]
    size_sprite = 43
    window = Tk()
    window.title("Mac_Gyver")
    maze = maze_load("level_1")
    (canvas, sprite_hero, photos) = maze_view(maze, window, size_sprite, pos_hero)
    init_touches(window, canvas, maze, pos_hero, sprite_hero,)
    window.mainloop()
