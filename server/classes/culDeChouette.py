import random
from collections import Counter
from random import choice
from random import sample
from classes.player import Player


class CulDeChouette:
    round_alive = True
    players = []
    score_max = 343
    score_min = 0
    currentPlayer = None
    moves = {
        "Chouette": 1,
        "Velute": 2,
        "Chouette Velute": 3,
        "Suite": 4,
        "Cul de Chouette": 5,
        "Néant": 6
    }

    # def __init__(self):
    #     self.players = []

    def roll_dice(self, numberDices):
        # print(f"{playerName} lance {numberDices} dès....")
        rolls = [random.randint(1, 6) for i in range(numberDices)]

        for index in range(len(rolls)):
            print(f"Le dés {index + 1} vaut {rolls[index]}")

        print(f"Le total du lancé est de {sum(rolls)}")
        
        # rolls = [3, 3, 5] #Chouette
        # rolls = [6, 6, 5] #Chouette 6
        # rolls = [2, 3, 5] #Velute
        # rolls = [3, 3, 6] #Chouette Velute
        # rolls = [6, 6, 6] #Cul de Chouette
        # rolls = [4, 5, 6] #Suite
        # rolls = [3, 4, 6] #Néant

        return rolls

    def createPlayers(self, players):
        i = 0
        for player in players:
            self.players.append(Player(player["name"], i))
            i += 1

    def party_config(self):
        number_players = -1
        
        while number_players < 2:
            # number_players = input("Combien de joueur vont disputer cette partie ? Minimum de 2 joueurs : ")

            try:
                number_players = int(number_players)
            except ValueError:
                return "Veuillez renseigner un nombre de joueurs valide !"
                number_players = -1
                continue
    
        # print(f"Le nombres de joueurs est de {number_players}")

        for id in range(1, number_players + 1):
            self.players.append(Player(f"Player{id}", id))
            # print(f"Le joueur {id} est crée !")
        
        print(self.players)
        return self.players

    def has_pair(self, dices):
        counting = Counter(dices)
        pairs = [k for k, v in counting.items() if v > 1]
        
        if not pairs:
            return False
        return pairs[0]

    def owl(self, pair):
        return pair * pair

    def velute(self, dices):
        if dices[0] + dices[1] == dices[2]:
            return (dices[2] * dices[2]) * 2
        
        return False

    def owl_velute(self, dices):

        randomPlayer = random.choice(self.players)
        print(f"{randomPlayer.name} est le 1er frappe dans ses mains et crie PAS MOU, LE CAILLOU !!")

        return randomPlayer
    
    def all_the_same_dices(self, dices):
        return not dices or [dices[0]] * len(dices) == dices

    def cul_de_chouette(self, dice_value):
        scoring = {1: 50, 2: 60, 3: 70, 4: 80, 5: 90, 6: 100}

        for index, score in scoring.items():
            if index == dice_value:
                return score

        return False
        
    def is_following(self, dices):
        return True if (dices[0 + 1] == dices[0] + 1) and (dices[0 + 2] == dices[0] + 2) else False

    def following_scoring(self):
        random_order = sample(self.players, len(self.players))
        for player in random_order:
            print(f"{player.name} frappe du poing sur la table et crie GRELOTTE CA PICOTE !!")
        
        print(f"Le dernier a avoir réussi l'enchainement est {random_order[-1].name}")
        last_player = filter(lambda player: player.id == random_order[-1].id, self.players)
        for player in last_player:
            player.remove_score(10)

    def use_civet(self):
        mise_max = 102
        print(f"{self.currentPlayer.name} utilise un de ses {self.currentPlayer.civet} Civets")

        if self.currentPlayer.score <= 0:
            print("Vous n'avez aucun points a miser !!")
            return False

        mise = 0
        while mise <= 0 or mise > mise_max:
            mise = input(f"Combien de vos {self.currentPlayer.score} points voulez vous miser ? Max {mise_max} points :")

            try:
                mise = int(mise)
            except ValueError:
                print("Vous n'avez pas rentré un nombre valide !")
                mise = -1
                continue
            if mise <= 0:
                print("Vous ne pouvez pas parier moins de rien !! :o")
            if mise > mise_max:
                print("Maximum 102 faut pas abuser non plus !! :o")

        print(f"{self.currentPlayer.name} utilise un Civet et mise {mise} de ses {self.currentPlayer.score} points !!")
        
        max_bet = list(self.moves.values())[-1]
        with_sipping = False
        bet = 0
        while bet <= 0 or bet > max_bet:
            bet = input(f"Veuillez selectionner votre pari sur votre prochain coup ! ({self.moves_to_string()}) : ")

            try:
                bet = int(bet)
            except ValueError:
                print("Veuillez entrer une valeur valide !")
                bet = -1
                continue
            if bet > max_bet or bet <= 0:
                print("Ce mouvement n'existe pas !!")
            # In case of chouette, with sipping or not
            if bet == 5:
                with_sipping = True if input("Preciser avec sirotage ou pas ? (y/n) : ") == 'y' else False
        
        print(f"{self.currentPlayer.name} pari que son prochain coup sera {list(self.moves.keys())[list(self.moves.values()).index(bet)]}")

        return bet, mise, with_sipping

    def moves_to_string(self):
        return ', '.join('{} : {}'.format(key, value) for key, value in self.moves.items())

    def get_move(self, value):
        return self.moves.get(list(self.moves.keys())[list(self.moves.values()).index(value)], 'Invalid value')

    def process_dices(self, dices, playerName):

        # for player in self.players:
        #     if player.name == playerName:
        #         self.currentPlayer = player

        print("processDiceCulDeChouetteClass", self.currentPlayer)
        pair = self.has_pair(dices)
        sipping = False
        # Cul de Chouette (all same dices)
        if self.all_the_same_dices(dices):
            print(f"Cul de Chouette !!")
            score = self.cul_de_chouette(dices[0])
            return 5
        # Following
        elif self.is_following(sorted(dices)):
            print(f"Suite !!")
            self.following_scoring()
            return 4
        # Chouette
        elif pair and not self.velute(dices):
            print(f"Chouette de {pair} !!")
            #Sirotage
            # sipping = True if input(f"{self.currentPlayer.name} fait Chouette de {pair} !! Voulez vous tentez un Cul de Chouette ?! (y/n): ") == 'y' else False
            # if sipping:
            #     self.sipping(pair)
            return 1
        # Velute
        elif self.velute(dices):
            print(f"Velute !!")
            # Chouette Velute
            if pair:
                print(f"Chouette Velute !!")
                return 3
            return 2
        #Neant
        else:
            print(f"Néant !!")
            return 6
    
    def getPlayers(self):
        return self.players

    def setCurrentPlayer(self, playerName):
        for player in self.players:
            if player.name == playerName:
                self.currentPlayer = player
        print(self.currentPlayer)
        return None

    def resetGame(self):
        self.players = []
        self.currentPlayer = None