from tkinter.messagebox import askquestion

""" The goal of the Assault class is to manage the interaction between the player and the guardian. """
class Assault:
    def __init__(self):
        """ Initializes the object with the value game_pursuit to true. This attribute will evolve during the game."""
        self.game_pursuit = True

    def assault(self, game, game_treasurs, game_mov):
        """The assault method aims to close the game in two different ways,
        depending on whether the player defeats the guardian or not. In any case,
        the player can replay or stop there."""
        if game_treasurs.treasurs[0] == 1 and game_treasurs.treasurs[1] == 2 and game_treasurs.treasurs[2] == 3:

            game.can.coords(game.sprite_hero, game_mov.pos_col + game_mov.pos_col * 43,
                            game_mov.pos_ligne + game_mov.pos_ligne * 43)
            del game.pos_hero[0]
            del game.pos_hero[0]
            game.pos_hero.append(game_mov.pos_col)
            game.pos_hero.append(game_mov.pos_ligne)
            game.can.delete(game.ennemy)
            game.infos.set("You defeat the guardian, you escape successfully!")
            self.endgame_win(game)

        elif game_treasurs.treasurs[0] != 1 or game_treasurs.treasurs[1] != 2 or game_treasurs.treasurs[2] != 3:
            self.endgame_lose(game)

    def endgame_lose(self, game):
        """The endgame_lose method is used in case the player has not gathered
        all the treasures to make the syringe and face the guardian."""
        result = askquestion("Loose", "You loose to pass the Guardian ! \n Wan't to try again ?", icon='warning')
        if result == 'yes':
            self.game_pursuit = True
            game.window.destroy()
        else:
            self.game_pursuit = False
            game.window.destroy()

    def endgame_win(self, game):
        """The endgame_win method is used in case the player has gathered
        all the treasures to make the syringe and face the guardian."""
        result = askquestion("Success !", "You pass the Guardian ! \n Wan't to try again ?", icon='warning')
        if result == 'yes':
            self.game_pursuit = True
            game.window.destroy()
        else:
            self.game_pursuit = False
            game.window.destroy()
