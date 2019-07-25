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

@app.route("/")
def helloWorld():
   return jsonify("Hello, cross-origin-world!")
   
@app.route('/startGame', methods=['POST'])
def start_game():
    players = request.get_json()['players']
    game.createPlayers(players)
    print(game.getPlayers())
    # session['players'] = json.dumps(game.getPlayers().__dict__)
    response = []
    
    for player in game.getPlayers():
        print(json.dumps(player).__dict__)
        session['playerName'] = player.name
        response.append({'name': player.name, 'score': player.score})
    return jsonify(response)

@app.route('/rollDices', methods=['POST'])
def rollDices():
    print("rollDicesRoute",actualPlayers)
    diceNumber = request.get_json()['dices']
    dices = game.roll_dice(3)

    return jsonify(dices)

@app.route('/processDices', methods=['POST'])
def processDices():
    dices = request.get_json()['dices']
    playerName = request.get_json()['playerName']
    resultDices = game.process_dices(dices, playerName)
    print("processDicesRoute",session.get('players'))

    if resultDices == 1:
        player.add_score(party.owl(pair), f"Chouette de {pair}")
    elif resultDices == 2:
        player.add_score(party.velute(roll_dices), "Velute")
    elif resultDices == 3:
        winner_owl_velute = party.owl_velute(roll_dices) 
        winner_owl_velute.add_score(party.velute(roll_dices), "Chouette Velute")
    elif resultDices == 4:
        party.following_scoring()
    elif resultDices == 5:
        player.add_score(party.cul_de_chouette(roll_dices[0]), "Cul de Chouette")
    elif resultDices == 6:
        player.add_grelottine()

    return jsonify(resultDices)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)