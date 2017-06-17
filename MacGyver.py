import os
import random
from tkinter import *



def maze_load(name) :

	"""Loads the maze from the file name.txt
	Name: name of the file containing the maze (without the extension .txt)
	Return data: a list with the maze data"""
	try :   #Try opening the desired file.
		fil = open(name + ".txt", "r") #Opens the "name" file read-only
		data = fil.readlines() #Stores the lines of the file in entries of the data list
		fil.close() #Closes the file after reading
	except IOError : #Raised if an I/O operation fails for an I/O-related reason
		print("Error importing file {}.txt".format(name)) #Error message
		os._exit(1) #Closing the script
	for i in range(len(data)) : #For each line read in data (len for the number of value in data.)
		data[i] = data[i].strip()# removes all whitespace at the start and end, including spaces, tabs, newlines and carriage returns.
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
	can = Canvas(window, width = 660, height = 660) #Definition of the dimensions of the window.
	photo_wall = PhotoImage(file = "sprites/wall.png") #Variable that stores the image of the wall.
	photo_treasure = PhotoImage(file = "sprites/treasure.png")#Variable that stores the image of the treasure.
	photo_ennemy = PhotoImage(file = "sprites/ennemy.png")#Variable that stores the image of the ennemy.
	photo_exit= PhotoImage(file = "sprites/exit.png")#Variable that stores the image of the exit.
	photo_hero= PhotoImage(file = "sprites/hero.png")#Variable that stores the image of the hero.


	n_line = 0 #Definition of a variable representing the line traveled. We start at the first line.
	for line in maze : #For each line in the list containing the maze
		n_col = 0 #Definition of a variable representing the column traveled. We start at the first character of the line.
		for car in line :#For each column in the actual line.
			# Walls
			if car == "+" or car == "-" or car == "|" :
				can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite,anchor = NW, image = photo_wall)
			# Treasurs
			elif car == "1" or car == "2" or car == "3" :
				can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite,anchor = NW, image = photo_treasure)
			# Ennemy
			elif car == "$" :
				can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite,anchor = NW, image = photo_ennemy)
			# Exit
			elif car == "O" :
				can.create_image(n_col + n_col * size_sprite, n_line + n_line * size_sprite,anchor = NW,image = photo_exit)
			n_col += 1
		n_line += 1

	# Hero display :
	sprite_hero = can.create_image(pos_hero[0] + pos_hero[0] * size_sprite,pos_hero[1] + pos_hero[1] * size_sprite,anchor = NW,image = photo_hero)
	
	can.pack()

	return (can, sprite_hero, {"hero": photo_hero,"wall": photo_wall,"treasure": photo_treasure,"ennemy" : photo_ennemy,"exit": photo_exit})



pos_hero = [1,1]
size_sprite = 43
fenetre = Tk()
fenetre.title("Mac_Gyver")
level = maze_load("level_1")
(canvas, sprite_perso, photos) = maze_view(level, fenetre,size_sprite, pos_hero)
fenetre.mainloop()