import os
from tkinter import *
import classes.mov_hero
import classes.treasures_gestion

""" 
The class Maze_init is the class that will allow to 
load the level provided as a parameter,
then to manage its display throughout the game. "
"""


class Maze_init:
    """
    It has several purposes, open the file containing the level,
     read it and store it in a list of lists named data.
    It must also create the window and loop TK and
    instantiate two objects, respectively game_mov
     from the Mov_hero class, and game_treasures from the Treasures_management class.
    After that, this function defines the position
     of the character with an attribute of the game_mov object.


    """
    def __init__(self, level_file):
        """Loads the maze from the file name.txt
               Name: name of the file containing the maze (without the extension .txt)
               Return data: a list with the maze data"""
        try:
            fil = open(level_file + ".txt", "r")
            self.data = fil.readlines()
            fil.close()
        except IOError:
            print("Error importing file {}.txt".format(level_file))
            os._exit(1)
        for i in range(len(self.data)):
            self.data[i] = self.data[i].strip()

        # Creation of the TK window with a title.
        self.window = Tk()
        self.window.title("Mac_Gyver")

        # Create an instance name game_treasures from Treasures_gestion object.
        self.game_treasures = classes.treasures_gestion.Treasures_gestion()

        # Create an instance name game_mov from Mov_hero object.
        self.game_mov = classes.mov_hero.Mov_hero()
        self.pos_hero = self.game_mov.pos_hero

        # Setting sprite size
        self.size_sprite = 43

        # Launch the game !
        (self.canvas, self.sprite_hero, self.photos) = self.maze_view(self.data, self.window, self.size_sprite,
                                                                      self.pos_hero)
        self.game_mov.init_touches(self.window, self.canvas, self.data, self.pos_hero, self.sprite_hero,
                                   self.game_treasures, self)

        # Creation of the information label.
        self.infos = StringVar()
        self.label = Label(self.window, textvariable=self.infos, bg="yellow").pack()
        self.infos.set("Start the game with Up, Down, Left and Right key !")

        # Creation of the inventory label.
        self.inventory = StringVar()
        self.label2 = Label(self.window, textvariable=self.inventory, bg="red").pack()
        self.inventory.set("This is your inventory, you need to craft"
                           " a sering in order to pass the guardian!")

        # Event loop
        self.window.mainloop()

    def maze_view(self, maze, window, size_sprite, pos_hero):
        """
        Display of a maze.
        maze: Variable containing the maze
        window: Graphic window
        size_sprite: Size of sprites in pixels
        pos hero: List containing the position of the character
        Return Value:
        Tuple containing the canvas, the sprite of the character and a
        Dictionary of images used for sprites
        """

        # Definition of the dimensions of the window.
        self.can = Canvas(window, width=660, height=660)
        # Variable that stores the image of the wall.
        self.photo_wall = PhotoImage(file="sprites/wall.png")
        # Variable that stores the image of the treasure.
        self.photo_treasure = PhotoImage(file="sprites/treasure.png")
        # Variable that stores the image of the ennemy.
        self.photo_ennemy = PhotoImage(file="sprites/ennemy.png")
        # Variable that stores the image of the exit.
        self.photo_exit = PhotoImage(file="sprites/exit.png")
        # Variable that stores the image of the hero.
        self.photo_hero = PhotoImage(file="sprites/hero.png")

        # Class method that defines the location of the treasures.
        self.game_treasures.random_treasure(self.data)

        n_line = 0  # Definition of a variable representing the line traveled.
        for line in maze:  # For each line in the list containing the maze
            n_col = 0  # Definition of a variable representing the column traveled.
            for car in line:  # For each column in the actual line.
                # Displays the walls.
                if car == "+" or car == "-" or car == "|":
                    self.can.create_image(n_col + n_col * self.size_sprite,
                                          n_line + n_line * self.size_sprite, anchor=NW,
                                          image=self.photo_wall)
                # Displays treasure 1, 2 and 3.
                elif car == "1":
                    self.treasure1 = self.can.create_image(n_col + n_col * self.size_sprite,
                                                           n_line + n_line * self.size_sprite, anchor=NW,
                                                           image=self.photo_treasure)
                elif car == "2":
                    self.treasure2 = self.can.create_image(n_col + n_col * self.size_sprite,
                                                           n_line + n_line * self.size_sprite, anchor=NW,
                                                           image=self.photo_treasure)
                elif car == "3":
                    self.treasure3 = self.can.create_image(n_col + n_col * self.size_sprite,
                                                           n_line + n_line * self.size_sprite, anchor=NW,
                                                           image=self.photo_treasure)
                # Displays the Ennemy.
                elif car == "$":
                    self.ennemy = self.can.create_image(n_col + n_col * self.size_sprite,
                                                        n_line + n_line * self.size_sprite,
                                                        anchor=NW,
                                                        image=self.photo_ennemy)
                # Displays the Exit
                elif car == "O":
                    self.can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite, anchor=NW,
                                          image=self.photo_exit)
                n_col += 1
            n_line += 1

        # Displays the Hero.
        self.sprite_hero = self.can.create_image(pos_hero[0] + pos_hero[0] * self.size_sprite,
                                                 pos_hero[1] + pos_hero[1] * self.size_sprite,
                                                 anchor=NW, image=self.photo_hero)
        # Integrates the display of images on canvas.
        self.can.pack()

        return (self.can, self.sprite_hero,
                {"hero": self.photo_hero, "wall": self.photo_wall, "treasure1": self.photo_treasure,
                 "ennemy": self.photo_ennemy,
                 "exit": self.photo_exit})
