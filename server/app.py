from flask import Flask, jsonify, request
from flask_cors import CORS
from classes.culDeChouette import CulDeChouette


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

game = CulDeChouette()
# actualPlayers = list({})

@app.route("/")
def helloWorld():
   return jsonify("Hello, cross-origin-world!")
   
@app.route('/startGame', methods=['POST'])
def start_game():
    players = request.get_json()['players']
    actualPlayers = game.createPlayers(players)
    response = []
    
    for player in game.getPlayers():
        print(player.score)
        response.append({'name': player.name, 'score': player.score})
    return jsonify(response)

@app.route('/rollDices', methods=['POST'])
def rollDices():
    print(request.get_json())
    diceNumber = request.get_json()['dices']
    dices = game.roll_dice(3)

    return jsonify(dices)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)