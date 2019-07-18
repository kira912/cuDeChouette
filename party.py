import random

class Player:
    score = 0

    def __init__(self, name):
        self.name = name


class CulDeChouette:
    round_alive = False
    dice1 = dice2 = dice3 = 0
    players = []


    @classmethod
    def roll_dice(self, number_dices):
        return [random.randint(1, 6) for i in range(number_dices)]

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
    
        print(f"Le nomnbres de joueurs est de {number_players}")

        for x in range(1, number_players + 1):
            self.players.append(Player(f"Player{x}"))
            print(f"Le joueur {x} est crée !")


def main():
    party = CulDeChouette()
    party.party_config()
    
    for player in party.players:
        roll_dices = party.roll_dice(3)
        print(f"{player.name} lance ses dès....")

        for index in range(len(roll_dices)):
            print(f"Le dés {index} vaut {roll_dices[index]}")




        exit()
main()