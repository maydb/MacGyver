import os
import random
from tkinter import *


def maze_load(name):
    """Loads the maze from the file name.txt
    Name: name of the file containing the maze (without the extension .txt)
    Return data: a list with the maze data"""
    try:  # Try opening the desired file.
        fil = open(name + ".txt", "r")  # Opens the "name" file read-only
        data = fil.readlines()  # Stores the lines of the file in entries of the data list
        fil.close()  # Closes the file after reading
    except IOError:  # Raised if an I/O operation fails for an I/O-related reason
        print("Error importing file {}.txt".format(name))  # Error message
        os._exit(1)  # Closing the script
    for i in range(len(data)):  # For each line read in data (len for the number of value in data.)
        data[i] = data[
            i].strip()  # removes all whitespace at the start and end, including spaces, tabs, newlines and carriage returns.
    return data


def maze_view(maze, window, size_sprite, pos_hero):
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
    can = Canvas(window, width=660, height=660)  # Definition of the dimensions of the window.
    photo_wall = PhotoImage(file="sprites/wall.png")  # Variable that stores the image of the wall.
    photo_treasure = PhotoImage(file="sprites/treasure.png")  # Variable that stores the image of the treasure.
    photo_ennemy = PhotoImage(file="sprites/ennemy.png")  # Variable that stores the image of the ennemy.
    photo_exit = PhotoImage(file="sprites/exit.png")  # Variable that stores the image of the exit.
    photo_hero = PhotoImage(file="sprites/hero.png")  # Variable that stores the image of the hero.

    n_line = 0  # Definition of a variable representing the line traveled. We start at the first line.
    for line in maze:  # For each line in the list containing the maze
        n_col = 0  # Definition of a variable representing the column traveled. We start at the first character of the line.
        for car in line:  # For each column in the actual line.
            # Walls
            if car == "+" or car == "-" or car == "|":
                can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite, anchor=NW,
                                 image=photo_wall)
            # Treasurs
            elif car == "1" or car == "2" or car == "3":
                can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite, anchor=NW,
                                 image=photo_treasure)
            # Ennemy
            elif car == "$":
                can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite, anchor=NW,
                                 image=photo_ennemy)
            # Exit
            elif car == "O":
                can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite, anchor=NW,
                                 image=photo_exit)
            n_col += 1
        n_line += 1

    # Hero display :
    sprite_hero = can.create_image(pos_hero[0] + pos_hero[0] * size_sprite, pos_hero[1] + pos_hero[1] * size_sprite,
                                   anchor=NW, image=photo_hero)

    can.pack()

    return (can, sprite_hero,
            {"hero": photo_hero, "wall": photo_wall, "treasure": photo_treasure, "ennemy": photo_ennemy,
             "exit": photo_exit})


def movement(event, can, mov, maze, pos_hero, hero):
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
    if mov == "left":
        pos_col -=1
    # Moving to the top  :
    if mov == "up":
        pos_ligne -=1
    # Moving to the bottom :
    if mov == "down":
        pos_ligne +=1

    # Test if the move leads the hero outside the playing area
    if pos_ligne < 0 or pos_col < 0 or pos_ligne > (n_lignes - 1) or pos_col > (n_cols - 1):
        return None
    # Otherwise if moving is possible on an empty square
    if maze[pos_ligne][pos_col] == " ":
        can.coords(hero, pos_col + pos_col * 43, pos_ligne + pos_ligne * 43)
        del pos_hero[0]
        del pos_hero[0]
        pos_hero.append(pos_col)
        pos_hero.append(pos_ligne)

def destroy(event, window) :
    """
    Closing the graphic window
    event: Object describing the event that triggered the call to this
    function Window: graphic window
    No return value"""
    window.destroy()

def init_touches(window, canvas, maze, pos_hero, hero) :
    """
    Initializing keyboard behavior
    canvas : Canvas where to display sprites
    maze : List containing the maze
    pos_hero :Current position of the hero
    Hero : Sprite representing the hero
    No return value
    """
    window.bind("<Right>", lambda event, can=canvas, l=maze, pos = pos_hero, p = hero: movement(event, can, "right", l, pos, p))
    window.bind("<Left>", lambda event, can=canvas, l= maze, pos=pos_hero, p=hero: movement(event, can, "left", l, pos, p))
    window.bind("<Up>", lambda event, can=canvas, l= maze, pos=pos_hero, p=hero: movement(event, can, "up", l, pos, p))
    window.bind("<Down>", lambda event, can=canvas, l= maze, pos=pos_hero, p=hero: movement(event, can, "down", l, pos, p))
    window.bind("<Escape>", lambda event, fen=window: destroy(event, fen))