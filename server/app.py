from flask import Flask, jsonify, request, session
from flask_cors import CORS
from classes.culDeChouette import CulDeChouette
import json


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'ABEEKvevfvfvfdgfbghbnfgnbgf'

# enable CORS
CORS(app)

game = CulDeChouette()
actualPlayers = []

@app.route('/startGame', methods=['POST'])
def start_game():
    players = request.get_json()['players']
    game.createPlayers(players)
    response = []
    
    for player in game.players:
        session['playerName'] = player.name
        response.append({'name': player.name, 'score': player.score})
    return jsonify(response)

@app.route('/rollDices', methods=['POST'])
def rollDices():
    diceNumber = request.get_json()['dices']
    dices = game.roll_dice(3)

    return jsonify(dices)

@app.route('/processDices', methods=['POST'])
def processDices():
    dices = request.get_json()['dices']
    playerName = request.get_json()['playerName']

    game.setCurrentPlayer(playerName)

    resultDices = game.process_dices(dices, playerName)
    player = game.currentPlayer
    pair = game.has_pair(dices)
    moveTranslated = list(game.moves.keys())[list(game.moves.values()).index(resultDices)]
    # print("frrte", game.moves.get(list(game.moves.values())[list(game.moves.values())], 'Invalid value'))

    response = {'move': moveTranslated, 'player': playerName}
    
    if player.score >= game.score_max:
        return jsonify({"hasWinner": True, "winner": player.name})

    if resultDices == 1:
        player.add_score(game.owl(pair), f"Chouette de {pair}")
    elif resultDices == 2:
        player.add_score(game.velute(dices), "Velute")
    elif resultDices == 3:
        winner_owl_velute = game.owl_velute(dices) 
        winner_owl_velute.add_score(game.velute(dices), "Chouette Velute")
    elif resultDices == 4:
        game.following_scoring()
    elif resultDices == 5:
        player.add_score(game.cul_de_chouette(dices[0]), "Cul de Chouette")
    elif resultDices == 6:
        player.add_grelottine()

    response['score'] = player.score
    return jsonify(response)

@app.route('/resetGame', methods=['GET'])
def resetGame():
    game.resetGame()
    return jsonify("RESET")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)