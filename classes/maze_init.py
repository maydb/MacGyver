import os
from tkinter import *
import classes.mov_hero
import classes.treasures_gestion

class Maze_init:
    def __init__(self, level_file):
        """Loads the maze from the file name.txt
               Name: name of the file containing the maze (without the extension .txt)
               Return data: a list with the maze data"""
        try:  # Try opening the desired file.
            fil = open(level_file + ".txt", "r")  # Opens the "name" file read-only
            self.data = fil.readlines()  # Stores the lines of the file in entries of the data list
            fil.close()  # Closes the file after reading
        except IOError:  # Raised if an I/O operation fails for an I/O-related reason
            print("Error importing file {}.txt".format(level_file))  # Error message
            os._exit(1)  # Closing the script
        for i in range(len(self.data)):  # For each line read in data (len for the number of value in data.)
            self.data[i] = self.data[i].strip()  # removes all whitespace at the start and end.

        self.window = Tk()
        self.window.title("Mac_Gyver")
        #self.treasurs = [0, 0, 0]  # List of treasures harvested !

        self.game_treasures = classes.treasures_gestion.Treasures_gestion()

        #self.pos_hero = [1, 1]

        #Creation of the Object game_mov who represent the Hero deplacement an initialization of is position.
        self.game_mov = classes.mov_hero.Mov_hero()
        self.pos_hero = self.game_mov.pos_hero


        #self.game_pursuit = True
        # Calculation of the size of the maze.


        self.size_sprite = 43
        (self.canvas, self.sprite_hero, self.photos) = self.maze_view(self.data, self.window, self.size_sprite,
                                                                      self.pos_hero)
        self.game_mov.init_touches(self.window, self.canvas, self.data, self.pos_hero, self.sprite_hero, self.game_treasures,self )

        self.infos = StringVar()
        self.label = Label(self.window, textvariable=self.infos, bg="yellow").pack()
        self.infos.set("Start the game with Up, Down, Left and Right key !")

        self.inventory = StringVar()
        self.label2 = Label(self.window, textvariable=self.inventory, bg="red").pack()
        self.inventory.set("This is your inventory, you need to craft a sering in order to pass the guardian!")

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
        self.can = Canvas(window, width=660, height=660)  # Definition of the dimensions of the window.
        self.photo_wall = PhotoImage(file="sprites/wall.png")  # Variable that stores the image of the wall.
        self.photo_treasure = PhotoImage(file="sprites/treasure.png")  # Variable that stores the image of the treasure.
        self.photo_ennemy = PhotoImage(file="sprites/ennemy.png")  # Variable that stores the image of the ennemy.
        self.photo_exit = PhotoImage(file="sprites/exit.png")  # Variable that stores the image of the exit.
        self.photo_hero = PhotoImage(file="sprites/hero.png")  # Variable that stores the image of the hero.

        self.game_treasures.random_treasure(self.data)

        n_line = 0  # Definition of a variable representing the line traveled. We start at the first line.
        for line in maze:  # For each line in the list containing the maze
            n_col = 0  # Definition of a variable representing the column traveled. We start at the first character of the line.
            for car in line:  # For each column in the actual line.
                # Walls
                if car == "+" or car == "-" or car == "|":
                    self.can.create_image(n_col + n_col * self.size_sprite, n_line + n_line * self.size_sprite,
                                          anchor=NW,
                                          image=self.photo_wall)
                elif car == "1":
                    global treasure1
                    self.treasure1 = self.can.create_image(n_col + n_col * self.size_sprite,
                                                           n_line + n_line * self.size_sprite, anchor=NW,
                                                           image=self.photo_treasure)
                elif car == "2":
                    global treasure2
                    self.treasure2 = self.can.create_image(n_col + n_col * self.size_sprite,
                                                           n_line + n_line * self.size_sprite, anchor=NW,
                                                           image=self.photo_treasure)
                elif car == "3":
                    global treasure3
                    self.treasure3 = self.can.create_image(n_col + n_col * self.size_sprite,
                                                           n_line + n_line * self.size_sprite, anchor=NW,
                                                           image=self.photo_treasure)
                # Ennemy
                elif car == "$":
                    self.ennemy = self.can.create_image(n_col + n_col * self.size_sprite, n_line + n_line * self.size_sprite,
                                          anchor=NW,
                                          image=self.photo_ennemy)
                # Exit
                elif car == "O":
                    self.can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite, anchor=NW,
                                          image=self.photo_exit)
                n_col += 1
            n_line += 1

        # Hero display :
        self.sprite_hero = self.can.create_image(pos_hero[0] + pos_hero[0] * self.size_sprite,
                                                 pos_hero[1] + pos_hero[1] * self.size_sprite,
                                                 anchor=NW, image=self.photo_hero)

        self.can.pack()

        return (self.can, self.sprite_hero,
                {"hero": self.photo_hero, "wall": self.photo_wall, "treasure1": self.photo_treasure,
                 "ennemy": self.photo_ennemy,
                 "exit": self.photo_exit})

