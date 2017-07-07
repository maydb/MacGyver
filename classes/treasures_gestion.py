import random

"""The Treasures Management class aims to deal with actions related to the discovery of treasures.
 It is notably in this class that it finds the inventory of the treasures."""
class Treasures_gestion():
    def __init__(self):
        """""We initialize a list containing the treasure inventory."""
        self.treasurs = [0, 0, 0]

    def random_treasure(self, maze):
        """This method allows to place the treasures randomly on the map, instead of a space."""
        treasurs_possible = 0
        data_of_void = []
        n_line = 0  # Definition of a variable representing the line traveled. We start at the first line.
        for line in maze:  # For each line in the list containing the maze
            n_col = 0  # Definition of a variable representing the column traveled.
            for car in line:
                if car == " ":
                    treasurs_possible += 1
                    data_of_void.append((n_line, n_col))
                n_col += 1
            n_line += 1

        treasur1_pos, treasur2_pos, treasur3_pos = random.sample(data_of_void, 3)

        maze[treasur1_pos[0]] = maze[treasur1_pos[0]][:treasur1_pos[1]] + "1" + maze[treasur1_pos[0]][
                                                                                treasur1_pos[1] + 1:]
        maze[treasur2_pos[0]] = maze[treasur2_pos[0]][:treasur2_pos[1]] + "2" + maze[treasur2_pos[0]][
                                                                                treasur2_pos[1] + 1:]
        maze[treasur3_pos[0]] = maze[treasur3_pos[0]][:treasur3_pos[1]] + "3" + maze[treasur3_pos[0]][
                                                                                treasur3_pos[1] + 1:]

    def find_treasure(self, treasure_id, game):
        """
        This method allows to place the treasures randomly on the map, instead of a space.
        """
        if treasure_id == game.treasure1:
            self.treasurs[0] = 1
            self.what_treasurs(treasure_id, game)
            self.how_many_treasurs(game)

        elif treasure_id == game.treasure2:
            self.treasurs[1] = 2
            self.what_treasurs(treasure_id, game)
            self.how_many_treasurs(game)

        elif treasure_id == game.treasure3:
            self.treasurs[2] = 3
            self.what_treasurs(treasure_id, game)
            self.how_many_treasurs(game)

    def what_treasurs(self, treasure_id, game):
        """On what treasures did the hero walk?"""
        if treasure_id == game.treasure1:
            game.infos.set("Congratulations ! You found a needle !")
        elif treasure_id == game.treasure2:
            game.infos.set("Congratulations ! You found a small plastic tube !")
        elif treasure_id == game.treasure3:
            game.infos.set("Congratulations ! You found ether !")

    def how_many_treasurs(self, game):
        """List the remaining treasures on the map."""
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

        game.inventory.set(go_craft)
