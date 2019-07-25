from classes.culDeChouette import CulDeChouette

def main():

    party = CulDeChouette()
    party.party_config()
    
    while party.round_alive:
        for player in party.players:

            if player.score >= party.score_max:
                print(f"{player.name} a gagné la partie !!")
                party.round_alive = False
                break
            result_roll = None
            bet_civet = 0
            party.current_player = player
            if player.available_civet() > 0:
                print(f"{player.name}, vous avez {player.civet} Civet disponible !")
                consume_civet = True if input("Voulez vous en utiliser un ? (y/n) : ") == 'y' else False

                if consume_civet:
                    bet_civet = party.use_civet(player)
                    print(bet_civet[1])

            # roll_dices = [3, 3, 5] #Chouette
            # roll_dices = [6, 6, 5] #Chouette 6
            # roll_dices = [2, 3, 5] #Velute
            roll_dices = [3, 3, 6] #Chouette Velute
            # roll_dices = [6, 6, 6] #Cul de Chouette
            # roll_dices = [4, 5, 6] #Suite
            # roll_dices = [3, 4, 6] #Néant

            # roll_dices = party.roll_dice(3)
            pair = party.has_pair(roll_dices)
            result_dices = party.process_dices(roll_dices)
            print(result_dices)

            if result_dices == 1:
                player.add_score(party.owl(pair), f"Chouette de {pair}")
            elif result_dices == 2:
                player.add_score(party.velute(roll_dices), "Velute")
            elif result_dices == 3:
                winner_owl_velute = party.owl_velute(roll_dices) 
                winner_owl_velute.add_score(party.velute(roll_dices), "Chouette Velute")
            elif result_dices == 4:
                party.following_scoring()
            elif result_dices == 5:
                player.add_score(party.cul_de_chouette(roll_dices[0]), "Cul de Chouette")
            elif result_dices == 6:
                player.add_grelottine()

            # result_roll = bet_civet[0]
            if bet_civet > 0 and result_roll == bet_civet[0]:
                print(f"{player.name} vient de réussir son Civet !! POPOPOPOPOPOPO quel medium !")
                player.add_score(bet_civet[1], "Civet")
            elif bet_civet < 0:
                print(f"{player.name} a échouer son Civet !!")
                player.remove_score(bet_civet[1])
            exit()
main()