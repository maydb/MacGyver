import os
import random
from tkinter import *
from tkinter.messagebox import askquestion


class Mac_Gyver:
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
        self.treasurs = [0, 0, 0]  # List of treasures harvested !
        self.pos_hero = [1, 1]


        self.game_pursuit = True
        # Calculation of the size of the maze.


        self.size_sprite = 43
        (self.canvas, self.sprite_hero, self.photos) = self.maze_view(self.data, self.window, self.size_sprite,
                                                                      self.pos_hero)
        self.init_touches(self.window, self.canvas, self.data, self.pos_hero, self.sprite_hero, )

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

        n_line = 0  # Definition of a variable representing the line traveled. We start at the first line.
        for line in maze:  # For each line in the list containing the maze
            n_col = 0  # Definition of a variable representing the column traveled. We start at the first character of the line.
            for car in line:  # For each column in the actual line.
                # Walls
                if car == "+" or car == "-" or car == "|":
                    self.can.create_image(n_col + n_col * self.size_sprite, n_line + n_line * self.size_sprite,
                                          anchor=NW,
                                          image=self.photo_wall)
                # Treasurs (we declare it has a global for delete it when macgyver found him.)
                if car == "1":
                    global treasure1
                    self.treasure1 = self.can.create_image(n_col + n_col * self.size_sprite,
                                                           n_line + n_line * self.size_sprite, anchor=NW,
                                                           image=self.photo_treasure)
                if car == "2":
                    global treasure2
                    self.treasure2 = self.can.create_image(n_col + n_col * self.size_sprite,
                                                           n_line + n_line * self.size_sprite, anchor=NW,
                                                           image=self.photo_treasure)
                if car == "3":
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

    def movement(self, event, can, mov, maze, pos_hero, hero):
        """
        Moving the hero !
        event:
        Object describing the event that triggered the call to this function.
        can : Canvas where to display the sprites.
        mov: Type of movement("up", "down", "left" or "right")
        maze: List containing the labyrinth
        Pos_hero: current position of the character
        hero : Sprite representing the character.
        No return value
        """
        n_cols = len(maze[0])
        n_lignes = len(maze)
        self.pos_col, self.pos_ligne = [self.pos_hero[0], self.pos_hero[1]]
        # Moving to the right :
        if mov == "right":
            self.pos_col += 1
        # Moving to the left :
        elif mov == "left":
            self.pos_col -= 1
        # Moving to the top  :
        elif mov == "up":
            self.pos_ligne -= 1
        # Moving to the bottom :
        elif mov == "down":
            self.pos_ligne += 1

        # Test if the move leads the hero outside the playing area
        if self.pos_ligne < 0 or self.pos_col < 0 or self.pos_ligne > (n_lignes - 1) or self.pos_col > (n_cols - 1):
            return None

        # Tests if a treasure is present on the next move. If so, remove the treasure and complete the hero's inventory.
        elif maze[self.pos_ligne][self.pos_col] == "1" or maze[self.pos_ligne][self.pos_col] == "2" or \
                        maze[self.pos_ligne][self.pos_col] == "3":
            if maze[self.pos_ligne][self.pos_col] == "1":
                self.find_treasure(self.treasure1)
                can.delete(self.treasure1)
            elif maze[self.pos_ligne][self.pos_col] == "2":
                self.find_treasure(self.treasure2)
                can.delete(self.treasure2)
            elif maze[self.pos_ligne][self.pos_col] == "3":
                self.find_treasure(self.treasure3)
                can.delete(self.treasure3)

            maze[self.pos_ligne] = maze[self.pos_ligne][:self.pos_col] + " " + maze[self.pos_ligne][self.pos_col + 1:]

            can.coords(hero, self.pos_col + self.pos_col * 43, self.pos_ligne + self.pos_ligne * 43)
            del pos_hero[0]
            del pos_hero[0]
            pos_hero.append(self.pos_col)
            pos_hero.append(self.pos_ligne)

            return [self.pos_col, self.pos_ligne]

        # Otherwise if moving is possible on an empty square
        elif maze[self.pos_ligne][self.pos_col] == " ":
            can.coords(hero, self.pos_col + self.pos_col * 43, self.pos_ligne + self.pos_ligne * 43)
            del self.pos_hero[0]
            del self.pos_hero[0]
            self.pos_hero.append(self.pos_col)
            self.pos_hero.append(self.pos_ligne)

        elif maze[self.pos_ligne][self.pos_col] == "$":
            self.assault()

    def find_treasure(self, treasure_id):
        """
        The function

        :param treasure_id:
        :return:
        """
        if treasure_id == self.treasure1:
            self.treasurs[0] = 1
            self.what_treasurs(treasure_id)
            self.how_many_treasurs()

        elif treasure_id == self.treasure2:
            self.treasurs[1] = 2
            self.what_treasurs(treasure_id)
            self.how_many_treasurs()

        elif treasure_id == self.treasure3:
            self.treasurs[2] = 3
            self.what_treasurs(treasure_id)
            self.how_many_treasurs()

    def what_treasurs(self, treasure_id):
        if treasure_id == self.treasure1:
            self.infos.set("Congratulations ! You found a needle !")
        elif treasure_id == self.treasure2:
            self.infos.set("Congratulations ! You found a small plastic tube !")
        elif treasure_id == self.treasure3:
            self.infos.set("Congratulations ! You found ether !")

    def how_many_treasurs(self):

        go_craft = ""

        treasure1_sent = "You still need a needle !\n"
        treasure2_sent = "You still need a small plastic tube !\n"
        treasure3_sent = "You still need ether !\n"
        all_treasurs_sent = "You craft a syringe ! You can put the guard to sleep !\n"



        if self.treasurs[0] == 0:
            go_craft += treasure1_sent
        if self.treasurs[1] == 0:
            go_craft += treasure2_sent
        if self.treasurs[2] == 0:
            go_craft += treasure3_sent
        elif self.treasurs[0] == 1 and self.treasurs[1] == 2 and self.treasurs[2] == 3:
            go_craft += all_treasurs_sent

        self.inventory.set(go_craft)

    def destroy(self, event, window):
        """
        Closing the graphic window
        event: Object describing the event that triggered the call to this
        function Window: graphic window
        No return value"""
        self.game_pursuit = False
        window.destroy()

    def init_touches(self, window, canvas, maze, pos_hero, hero):
        """
        Initializing keyboard behavior
        canvas : Canvas where to display sprites
        maze : List containing the maze
        pos_hero :Current position of the hero
        Hero : Sprite representing the hero
        No return value
        """
        self.window.bind("<Right>",
                         lambda event, can=canvas, l=maze, pos=pos_hero, p=hero: self.movement(event, can, "right", l,
                                                                                               pos, p))
        self.window.bind("<Left>",
                         lambda event, can=canvas, l=maze, pos=pos_hero, p=hero: self.movement(event, can, "left", l,
                                                                                               pos, p))
        self.window.bind("<Up>",
                         lambda event, can=canvas, l=maze, pos=pos_hero, p=hero: self.movement(event, can, "up", l, pos,
                                                                                               p))
        self.window.bind("<Down>",
                         lambda event, can=canvas, l=maze, pos=pos_hero, p=hero: self.movement(event, can, "down", l,
                                                                                               pos, p))
        self.window.bind("<Escape>", lambda event, fen=window: self.destroy(event, fen))

    def assault(self):
        if self.treasurs[0] == 1 and self.treasurs[1] == 2 and self.treasurs[2] == 3:

            self.can.coords(self.sprite_hero, self.pos_col + self.pos_col * 43, self.pos_ligne + self.pos_ligne * 43)
            del self.pos_hero[0]
            del self.pos_hero[0]
            self.pos_hero.append(self.pos_col)
            self.pos_hero.append(self.pos_ligne)
            self.can.delete(self.ennemy)
            self.infos.set("You defeat the guardian ! Escape Now !")

        elif self.treasurs[0] != 1 or self.treasurs[1] != 2 and self.treasurs[2] != 3:
            self.endgame()

    def endgame(self):
        result = askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            self.game_pursuit = True
            self.window.destroy()
        else:
            self.game_pursuit = False
            self.window.destroy()
