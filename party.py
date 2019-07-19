import random
from collections import Counter

class Player:
    score = 0
    name = ""

    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def add_score(self, score):
        self.score += score
        print(f"{self.name} vient d'obtenir {score}, son score est desormais de {self.score}")

    @classmethod
    def remove_score(self, score):
        self.score -= score


class CulDeChouette:
    round_alive = False
    dice1 = dice2 = dice3 = 0
    players = []


    @classmethod
    def roll_dice(self, player, number_dices):
        print(f"{player.name} lance ses dès....")
        rolls = [random.randint(1, 6) for i in range(number_dices)]

        for index in range(len(rolls)):
            print(f"Le dés {index + 1} vaut {rolls[index]}")

        print(f"Le total du lancé est de {sum(rolls)}")
        
        return rolls

    @classmethod
    def party_config(self):
        number_players = -1
        
        while number_players < 2:
            number_players = input("Combien de joueur vont disputer cette partie ? Minimum de 2 joueurs : ")

            try:
                number_players = int(number_players)
            except ValueError:
                print("Veuillez renseigner un nombre de joueurs valide !")
                number_players = -1
                continue
    
        print(f"Le nombres de joueurs est de {number_players}")

        for id in range(1, number_players + 1):
            self.players.append(Player(f"Player{id}", id))
            print(f"Le joueur {id} est crée !")
        
        return True

    @classmethod
    def has_pair(self, dices):
        counting = Counter(dices)
        return [k for k, v in counting.items() if v > 1]

    @classmethod
    def owl(self, pair):
        return pair * pair

    @classmethod
    def velute(self, dices):
        if dices[0] + dices[1] == dices[2]:
            return (dices[2] * dices[2]) * 2
        
        return False

    @classmethod
    def owl_velute(self, dices):

        rand = random.randint(1, len(self.players))
        print(f"Player{rand} est le 1er frappe dans ses mains et crie PAS MOU, LE CAILLOU !!")
        player_win = filter(lambda player: player.id == rand, self.players)
        
        for player in player_win:
            player.add_score(self.velute(dices))
    
    def all_the_same_dices(self, dices):
        return not dices or [dices[0]] * len(dices) == dices

    def cul_de_chouette(self, dice_value):
        min_scoring = 50
        



def main():
    party = CulDeChouette()
    party.party_config()
    
    for player in party.players:
        # roll_dices = party.roll_dice(player, 3)
        roll_dices = [3, 3, 3]
        pair = party.has_pair(roll_dices)
        
        # Chouette
        if pair and not party.velute(roll_dices):
            owl_result = party.owl(pair[0])
            player.add_score(owl_result)
        
        # Velute
        if party.velute(roll_dices):
            if not pair:
                player.add_score(party.velute(roll_dices))

            # Chouette Velute
            party.owl_velute(roll_dices)

        if party.all_the_same_dices(roll_dices):

        

        exit()
main()