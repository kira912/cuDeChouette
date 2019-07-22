import random
from collections import Counter
from random import choice
from random import sample

class Player:
    score, civet, grelottine = 0, 1, 0
    name = ""

    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def add_score(self, score, by):
        self.score += score
        print(f"{self.name} vient d'obtenir {score} grace a {by}, son score est desormais de {self.score}")

    def remove_score(self, score):
        self.score -= score

        if self.score < 0:
            self.score = 0
        print(f"{self.name} vient de perdre {score} son score est desormais de {self.score}")

    def add_civet(self):
        self.civet += 1

    def add_grelottine(self):
        if self.grelottine > 0:
            print(f"{self.name} possède déjà une Grelottine")
            return
        print(f"{self.name} vient de gagner une Grelottine")
        self.grelottine = 1

    def available_civet(self):
        return self.civet

class CulDeChouette:
    round_alive = False
    players = []
    score_max = 343
    score_min = 0
    # dice1 = dice2 = dice3 = 0


    @classmethod
    def roll_dice(self, player, number_dices):
        print(f"{player.name} lance {number_dices} dès....")
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
        pairs = [k for k, v in counting.items() if v > 1]
        
        if not pairs:
            return False
        return pairs[0]

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
            player.add_score(self.velute(dices), "Chouette Velute")
    
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

    def sipping(self, current_player, pair):

        if pair == 6:
            print("Possibilité de gagner un Civet !")

        bet = {current_player.name: pair}
        for player in self.players:
            if player.name == current_player.name:
                continue

            rand = random.randint(1, 6)
            while rand in bet.values():
                rand = random.randint(1, 6)
            print(f"{player.name} choisi le {rand}")
            bet.update({player.name : rand})
        
        # random_roll = pair
        # random_roll = 8
        # random_roll = bet['Player2']
        random_roll = self.roll_dice(current_player, 1)[0]
        try:
            winner = list(bet.keys())[list(bet.values()).index(random_roll)]
        except ValueError:
            print("Personne ne remporte son pari !")
            current_player.remove_score(self.owl((pair)))

            print(f"{current_player.name} gagne 1 Civet !")
            current_player.add_civet()
            return False

        if winner == current_player.name:
            print(f"{current_player.name} réussi son Sirotage !!")
            current_player.add_score(self.cul_de_chouette(pair), "Sirotage")
        else:
            print(f"{winner} rafle la mise !!")
            winner = list(filter(lambda player: player.name == winner, self.players))[0]
            winner.add_score(25, "Sirotage")

            print(f"{current_player.name} gagne 1 Civet !")
            current_player.add_civet()

    def use_civet(self, player):
        mise_max = 102
        print(f"{player.name} utilise un de ses {player.civet} Civets")

        mise = input(f"Combien de vos {player.score} points voulez vous miser ? Max {mise_max} points :")

def main():
    party = CulDeChouette()
    party.party_config()
    
    for player in party.players:

        if player.available_civet() > 0:
            print(f"Vous avez {player.civet} Civet disponible !")
            consume_civet = True if input("Voulez vous en utiliser un ? (y/n) : ") == 'y' else False

            if consume_civet:
                party.use_civet(player)
                exit()
        roll_dices = party.roll_dice(player, 3)

        # roll_dices = [3, 3, 5] #Chouette
        # roll_dices = [2, 3, 5] #Velute
        # roll_dices = [3, 3, 6] #Chouette Velute
        # roll_dices = [6, 6, 6] #Cul de Chouette
        # roll_dices = [4, 5, 6] #Suite
        # roll_dices = [3, 4, 6] #Néant
        pair = party.has_pair(roll_dices)
        
        # Cul de Chouette (all same dices)
        if party.all_the_same_dices(roll_dices):
            score = party.cul_de_chouette(roll_dices[0])
            player.add_score(score, "Cul de Chouette")
            break
        
        # Following
        elif party.is_following(sorted(roll_dices)):
            party.following_scoring()
            break

        # Chouette
        elif pair and not party.velute(roll_dices):

            #Sirotage
            retry_last_dice = True if input(f"{player.name} fait Chouette de {pair} !! Voulez vous tentez un Cul de Chouette ?! (y/n): ") == 'y' else False
            if retry_last_dice:
                party.sipping(player, pair)
                break
            else:
                owl_result = party.owl(pair)
                player.add_score(owl_result, f"Chouette de {pair}")
                break
        
        # Velute
        elif party.velute(roll_dices):
            # Chouette Velute
            if pair:
                party.owl_velute(roll_dices)
                break
            player.add_score(party.velute(roll_dices), "Velute")
            break
        #Neant, Cannot make action with roll dices
        else:
            player.add_grelottine()
            break

        exit()
main()