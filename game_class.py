import os
import random
from tkinter import *



class Mac_Gyver:

    def __init__(self,level_file):
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
        self.pos_hero = [1, 1]
        self.size_sprite = 43
        (self.canvas, self.sprite_hero, self.photos) = self.maze_view(self.data, self.window, self.size_sprite, self.pos_hero)
        self.init_touches(self.window, self.canvas, self.data, self.pos_hero, self.sprite_hero,)
        self.window.mainloop()


    def maze_view(self,maze, window, size_sprite, pos_hero):
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
                    self.can.create_image(n_col + n_col * self.size_sprite, n_line + n_line * self.size_sprite, anchor=NW,
                                     image=self.photo_wall)
                # Treasurs (we declare it has a global for delete it when macgyver found him.)
                if car =="1":
                    global treasurs1
                    self.treasurs1 = self.can.create_image(n_col + n_col * self.size_sprite, n_line + n_line * self.size_sprite, anchor=NW,
                                     image=self.photo_treasure)
                if car == "2":
                    global treasurs2
                    self.treasurs2 = self.can.create_image(n_col + n_col * self.size_sprite, n_line + n_line * self.size_sprite, anchor=NW,
                                                     image=self.photo_treasure)
                if car == "3":
                    global treasurs3
                    self.treasurs3 = self.can.create_image(n_col + n_col * self.size_sprite, n_line + n_line * self.size_sprite, anchor=NW,
                                                     image=self.photo_treasure)


                # Ennemy
                elif car == "$":
                    self.can.create_image(n_col + n_col * self.size_sprite, n_line + n_line * self.size_sprite, anchor=NW,
                                     image=self.photo_ennemy)
                # Exit
                elif car == "O":
                    self.can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite, anchor=NW,
                                     image=self.photo_exit)
                n_col += 1
            n_line += 1

        # Hero display :
        self.sprite_hero = self.can.create_image(pos_hero[0] + pos_hero[0] * self.size_sprite, pos_hero[1] + pos_hero[1] * self.size_sprite,
                                       anchor=NW, image=self.photo_hero)

        self.can.pack()

        return (self.can, self.sprite_hero,
                {"hero": self.photo_hero, "wall": self.photo_wall, "treasure1": self.photo_treasure, "ennemy": self.photo_ennemy,
                 "exit": self.photo_exit})


    def movement(self,event, can, mov, maze, pos_hero, hero):
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
        # Calculation of the size of the maze.
        n_cols = len(maze[0])
        n_lignes = len(maze)
        pos_col, pos_ligne = [pos_hero[0], pos_hero[1]]
        # Moving to the right :
        if mov == "right" :
            pos_col += 1
        # Moving to the left :
        elif mov == "left":
            pos_col -=1
        # Moving to the top  :
        elif mov == "up":
            pos_ligne -=1
        # Moving to the bottom :
        elif mov == "down":
            pos_ligne +=1

        # Test if the move leads the hero outside the playing area
        if pos_ligne < 0 or pos_col < 0 or pos_ligne > (n_lignes - 1) or pos_col > (n_cols - 1):
            return None

        #Tests if a treasure is present on the next move. If so, remove the treasure and complete the hero's inventory.
        elif maze[pos_ligne][pos_col] == "1" or maze[pos_ligne][pos_col] == "2" or maze[pos_ligne][pos_col] == "3":
            if maze[pos_ligne][pos_col] == "1" :
                can.delete(self.treasurs1)
            elif maze[pos_ligne][pos_col] == "2" :
                can.delete(self.treasurs2)
            elif maze[pos_ligne][pos_col] == "3" :
                can.delete(self.treasurs3)

            maze[pos_ligne] = maze[pos_ligne][:pos_col] +" "+maze [pos_ligne][pos_col + 1:]

            can.coords(hero, pos_col + pos_col * 43, pos_ligne + pos_ligne * 43)
            del pos_hero[0]
            del pos_hero[0]
            pos_hero.append(pos_col)
            pos_hero.append(pos_ligne)

            return [pos_col, pos_ligne]

        # Otherwise if moving is possible on an empty square
        elif maze[pos_ligne][pos_col] == " ":
            can.coords(hero, pos_col + pos_col * 43, pos_ligne + pos_ligne * 43)
            del pos_hero[0]
            del pos_hero[0]
            pos_hero.append(pos_col)
            pos_hero.append(pos_ligne)

    def destroy(self,event, window ) :
        """
        Closing the graphic window
        event: Object describing the event that triggered the call to this
        function Window: graphic window
        No return value"""
        window.destroy()

    def init_touches(self,window, canvas, maze, pos_hero, hero) :
        """
        Initializing keyboard behavior
        canvas : Canvas where to display sprites
        maze : List containing the maze
        pos_hero :Current position of the hero
        Hero : Sprite representing the hero
        No return value
        """
        self.window.bind("<Right>", lambda event, can=canvas, l=maze, pos = pos_hero, p = hero: self.movement(event, can, "right", l, pos, p))
        self.window.bind("<Left>", lambda event, can=canvas, l= maze, pos=pos_hero, p=hero: self.movement(event, can, "left", l, pos, p))
        self.window.bind("<Up>", lambda event, can=canvas, l= maze, pos=pos_hero, p=hero: self.movement(event, can, "up", l, pos, p))
        self.window.bind("<Down>", lambda event, can=canvas, l= maze, pos=pos_hero, p=hero: self.movement(event, can, "down", l, pos, p))
        self.window.bind("<Escape>", lambda event, fen=window: self.destroy(event, fen))