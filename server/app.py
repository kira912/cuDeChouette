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
        response.append({'name': player.name, 'score': player.score, 'launched': player.launched})
    return jsonify(response)

@app.route('/rollDices', methods=['POST'])
def rollDices():
    diceNumber = request.get_json()['dices']
    dices = game.roll_dice(diceNumber)

    return jsonify(dices)

@app.route('/processDices', methods=['POST'])
def processDices():
    dices = request.get_json()['dices']
    playerName = request.get_json()['playerName']

    game.setCurrentPlayer(playerName)
    game.currentPlayer.launched += 1

    resultDices = game.process_dices(dices, playerName)
    player = game.currentPlayer
    pair = game.has_pair(dices)
    moveTranslated = list(game.moves.keys())[list(game.moves.values()).index(resultDices)]

    response = {'move': moveTranslated, 'player': playerName}
    
    if player.score >= game.score_max:
        return jsonify({"hasWinner": True, "winner": player.name})

    response['score'] = player.score
    response['launched'] = player.launched
    response['move'] = moveTranslated
    response['player'] = playerName

    return jsonify(response)

@app.route('/addScore', methods=['POST'])
def addScore():
    playerName = request.get_json()['playerName']
    move = request.get_json()['move']
    dices = request.get_json()['dices']

    pair = game.has_pair(dices)

    filtering = filter(lambda player: player.name == playerName, game.players)
    response = {}

    if filtering:
        for player in filtering:
            moveToInt = game.moves.get(move)
            if moveToInt == 1:
                player.add_score(game.owl(pair), f"game.get_move(moveToInt) de {pair}")
            elif moveToInt == 2:
                player.add_score(game.velute(dices), game.get_move(moveToInt))
            elif moveToInt == 3:
                winner_owl_velute = game.owl_velute(dices) 
                winner_owl_velute.add_score(game.velute(dices), game.get_move(moveToInt))
            elif moveToInt == 4:
                game.following_scoring()
            elif moveToInt == 5:
                player.add_score(game.cul_de_chouette(dices[0]), game.get_move(moveToInt))
            elif moveToInt == 6:
                player.add_grelottine()
            # player.add_score(score, "Sirotage")
            response['playerName'] = player.name
            response['score'] = player.score
    
    return jsonify(response)

@app.route('/resetGame', methods=['GET'])
def resetGame():
    game.resetGame()
    return jsonify("RESET")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)