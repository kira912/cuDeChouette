<template>
  <v-container>
    <div v-if="!playerCreated">
      <h1>{{ msg }}</h1>
      <p>{{ numberPlayersText }}</p>
      <v-layout align-center justify-center row v-for="player in players">
        <v-flex xs12 sm6 md3>
          <v-text-field outlined v-model="player.name"></v-text-field>
        </v-flex>
      </v-layout>
      <v-btn color="primary" @click="addPlayer()">{{ addPlayerText }}</v-btn>
      <!-- <v-btn v-if="players.length < 2" disabled color="primary" @click="startGame()"> {{ textButton }}</v-btn> -->
      <v-btn color="primary" @click="startGame()">{{ textButton }}</v-btn>
    </div>
    <v-container v-else class="background">
      <h1>Cul de Chouette Game</h1>
      <v-layout wrap>
        <v-flex pa-1>
          <v-btn color="primary" @click="resetGame()">Reset Game</v-btn>
          <v-parallax :src="require('@/assets/green.jpg')" height="1000">
            <transition name="slide-title">
              <v-layout row id="dice" justify-center justify-space-around>
                <div v-if="dices" v-for="dice in dices">
                  <v-img :src="showDiceImage(dice)" height="100px" width="100px"></v-img>
                </div>
              </v-layout>
            </transition>

            <v-dialog v-model="activeSippingModal" max-width="500" justify-center>
              <v-card>
                <v-card-title>{{ dicesProcessing.player }} veut il tenter son Cul de Chouette ?</v-card-title>
                <v-spacer></v-spacer>

                <v-btn color="primary" @click="activateSipping(), activeSippingModal = false">Oui</v-btn>
                <v-btn color="danger" @click="addScore(), activeSippingModal = false">Non</v-btn>
              </v-card>
            </v-dialog>

            <h1 v-if="hasWinner">{{ winnerMsg }}</h1>
            <v-layout>
              <v-flex>
                <h1 v-if="dices.length > 0 && !activeSipping">TOTAL des 3 dès : {{ sumDices }}</h1>
                <h1 v-if="activeSipping">TOTAL du lancé de sirotage : {{ dices[2] }}</h1>
              </v-flex>
              <v-flex>
                <h1>{{ getMove }}</h1>
              </v-flex>
            </v-layout>
          </v-parallax>
        </v-flex>
        <v-flex shrink ma-5>
          <v-card
            v-for="player in players"
            :key="player.name"
            :id="player.name"
            v-model="sippingBet"
          >
            <v-layout column pa-5>
              <v-card-text class="font-weight-bold display-1">{{ player.name }}</v-card-text>
              <v-card-text class="font-weight-bold">Score : {{ player.score }}</v-card-text>
              <v-text-field
                v-if="activeSipping"
                persistent-hint
                :hint="player.hint"
                type="number"
                outlined
                min="1"
                max="6"
                :rules="[ruleInputSipping.minMax]"
                v-model="player.bet"
                :disabled="player.disableSippingInput"
              ></v-text-field>
              <v-btn
                v-if="!hasWinner"
                color="primary"
                @click="rollDices(3, player.name)"
              >Lancer les dès</v-btn>
            </v-layout>
          </v-card>
          <v-layout ma-5>
            <v-btn
              v-if="activeSipping"
              color="warning"
              :disabled="validateBets"
              @click="sipping()"
            >Valider les paris</v-btn>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-container>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Homepage",
  data() {
    return {
      msg: "Bienvenue dans le Cul de Chouette!",
      textButton: "Commencer une partie",
      numberPlayersText: "Veuillez renseigner les noms des joueurs",
      addPlayerText: "Ajouter un joueur",
      players: [],
      playerCreated: false,
      dices: [],
      dicesProcessing: {
        player: null,
        move: "",
        score: 0
      },
      activeSipping: false,
      activeSippingModal: false,
      ruleInputSipping: {
        minMax: v =>
          (v >= 1 && v <= 6) ||
          "Tu utilises des dès a combien de face connard ?"
      },
      sippingDice: 0,
      hasWinner: false,
      winnerMsg: ""
    };
  },
  computed: {
    sumDices() {
      return this.dices.reduce((a, b) => {
        return a + b;
      });
    },
    getMove() {
      let move = this.dicesProcessing.move
        ? this.dicesProcessing.move
        : "En attente";

      if (move == "Chouette") {
        move += " de " + this.getPair();
      } else if (move == "Velute") {
        move += ` de ${this.dices[2]}`;
      }

      return move;
    },
    sippingBet: {
      get() {},
      set(newValue) {
        this.players.find(player => {
          if (player.name != this.dicesProcessing.player) {
            player.disableSippingInput = false;
            player.bet = newValue.data;
            player.hint = "Veuillez choisir entre 1 et 6";
          }
        });
      }
    },

    // Return false if if all bets is ok for remove disabled property og button (vuetify)
    validateBets() {
      let bets = [];
      this.players.forEach(player => {
        if (player.bet != null) {
          bets.push(player.bet);
        }
      });

      return bets.length === this.players.length ? false : true;
    },
    whoTheNext() {}
  },

  methods: {
    getPair() {
      const count = names =>
        names.reduce((a, b) => ({ ...a, [b]: (a[b] || 0) + 1 }), {});

      const duplicates = dict => Object.keys(dict).filter(a => dict[a] > 1);

      return duplicates(count(this.dices))[0];
    },

    startGame() {
      const path = "http://localhost:5000/startGame";
      axios
        .post(path, {
          players: this.players
        })
        .then(response => {
          this.players = response.data;
          this.playerCreated = true;
        })
        .catch(err => {
          console.error(err);
        });
    },

    addPlayer: function() {
      this.players.push({ name: "", score: 0, bet: 0 });
    },

    rollDices(numberToRolls, name) {
      const path = "http://localhost:5000/rollDices";
      axios
        .post(path, {
          dices: numberToRolls
        })
        .then(response => {
          this.dices = response.data;
          this.sippingDice = response.data.length == 1 ? response.data : 0;

          if (!this.activeSipping) {
            this.processDices(this.dices, name);
          }
          // if (this.dices.length == 3) {
          //   this.processDices(this.dices, name);
          // }
        })
        .catch(err => {
          console.error(err);
        });
    },

    processDices(dices, name) {
      this.dicesProcessing.player = name;
      const path = "http://localhost:5000/processDices";
      axios
        .post(path, {
          dices: dices,
          playerName: name
        })
        .then(response => {
          console.log("ProcessDiceRoute", response.data);
          this.dicesProcessing.move = response.data.move;
          if (response.data.move == "Chouette") {
            this.activeSippingModal = true;
          } else {
            this.addScore();
          }

          if (response.data.hasWinner) {
            this.hasWinner = true;
            this.winner(response.data.winner);
          }
          this.players.find(player => {
            if (player.name == response.data.player) {
              (player.score = response.data.score),
                (player.launched = response.data.launched);
            }
          });
          this.dicesProcessing = response.data;
        })
        .catch(err => {
          console.error(err);
        });
    },

    addScore() {
      const path = "http://localhost:5000/addScore";

      axios
        .post(path, {
          move: this.dicesProcessing.move,
          playerName: this.dicesProcessing.player,
          dices: this.dices
        })
        .then(response => {
          this.players.find(player => {
            if (player.name == response.data.playerName) {
              player.score = response.data.score;
            }
          });
        })
        .catch(err => {
          console.error(err);
        });
    },

    sipping() {
      const rollDiceSippingPath = "http://localhost:5000/rollDices";
      axios
        .post(rollDiceSippingPath, {
          dices: 1
        })
        .then(response => {
          //TODO force dice for test, don't forget to remove this shit :D
          const diceRolled = response.data;
          this.dices[2] = diceRolled;
          if (this.dices.includes(diceRolled)) {
            this.dicesProcessing.move = "Cul de Chouette !!";
            this.addScore(this.dices[2] * this.dices[2]);
          }

          this.activeSipping = false;
        })
        .catch(error => {
          console.log(error);
        });
    },

    activateSipping() {
      this.activeSipping = true;

      this.players.find(player => {
        if (player.name == this.dicesProcessing.player) {
          player.disableSippingInput = true;
          player.bet = this.getPair();
          player.hint =
            "Vous ne pouvez pas choisir vous tenter un Cul de Chouette";
        }
      });
    },

    winner(name) {
      this.winnerMsg = `${name} a remporté la partie !`;
    },

    resetGame() {
      const path = "http://localhost:5000/resetGame";
      axios
        .get(path)
        .then(response => {
          console.log(response);
        })
        .catch(err => {
          console.error(err);
        });
    },

    checkBetPlayers() {
      let bets = [];
      this.players.forEach(player => {
        if (player.bet != null) {
          bets.push(player.bet);
        }
      });

      return bets.length === this.players.length ? true : false;
    },

    showDiceImage: function(dice) {
      if (dice === 1) {
        return "http://i.imgur.com/6knk862.png";
      }

      if (dice === 2) {
        return "http://i.imgur.com/ik7dK9D.png";
      }

      if (dice === 3) {
        return "http://i.imgur.com/sh0H0td.png";
      }

      if (dice === 4) {
        return "http://i.imgur.com/1GPkhq3.png";
      }

      if (dice === 5) {
        return "http://i.imgur.com/bINitmy.png";
      }

      if (dice === 6) {
        return "http://i.imgur.com/6qXMSrt.png";
      }
      return "http://i.imgur.com/6knk862.png";
    }
  }
};
</script>

<style scoped>
#dice v-img {
  width: 50px;
}
.text-field-size {
  width: 25%;
}

.bakground {
  max-width: 50%;
}

.slide-title-leave-active,
.slide-title-enter-active {
  transition: 7s ease-out;
}
.slide-title-enter {
  transform: translate(+100%);
}
</style>
