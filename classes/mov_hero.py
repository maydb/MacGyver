import classes.assault


class Mov_hero :

    def __init__(self):
        self.pos_hero = [1, 1]
        self.combat = classes.assault.Assault()

    def movement(self, event, can, mov, maze, pos_hero, hero,game_treasures,game):
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
                game_treasures.find_treasure(game.treasure1,game)
                can.delete(game.treasure1)
            elif maze[self.pos_ligne][self.pos_col] == "2":
                game_treasures.find_treasure(game.treasure2,game)
                can.delete(game.treasure2)
            elif maze[self.pos_ligne][self.pos_col] == "3":
                game_treasures.find_treasure(game.treasure3,game)
                can.delete(game.treasure3)

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
            self.combat.assault(game,game_treasures,self)

    def init_touches(self, window, canvas, maze, pos_hero, hero,game_treasures,game):
            """
            Initializing keyboard behavior
            canvas : Canvas where to display sprites
            maze : List containing the maze
            pos_hero :Current position of the hero
            Hero : Sprite representing the hero
            No return value
            """
            window.bind("<Right>",
                             lambda event, can=canvas, l=maze, pos=pos_hero, p=hero: self.movement(event, can, "right",
                                                                                                   l,
                                                                                                   pos, p,game_treasures,game))
            window.bind("<Left>",
                             lambda event, can=canvas, l=maze, pos=pos_hero, p=hero: self.movement(event, can, "left",
                                                                                                   l,
                                                                                                   pos, p,game_treasures,game))
            window.bind("<Up>",
                             lambda event, can=canvas, l=maze, pos=pos_hero, p=hero: self.movement(event, can, "up", l,
                                                                                                   pos,
                                                                                                   p,game_treasures,game))
            window.bind("<Down>",
                             lambda event, can=canvas, l=maze, pos=pos_hero, p=hero: self.movement(event, can, "down",
                                                                                                   l,
                                                                                                   pos, p,game_treasures,game))
            window.bind("<Escape>", lambda event, fen=window: self.destroy(event, fen))

    def destroy(self, event, window):
        """
        Closing the graphic window
        event: Object describing the event that triggered the call to this
        function Window: graphic window
        No return value"""
        self.combat.game_pursuit = False
        window.destroy()