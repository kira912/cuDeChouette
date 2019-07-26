<template>
  <v-container>
    <div v-if="!playerCreated">
      <h1>{{ msg }}</h1>
      <p>{{ numberPlayersText }}</p>
      <v-layout
        align-center
        justify-center
        row
        v-for="player in players"
      >
        <v-flex xs12 sm6 md3>
          <v-text-field outlined v-model="player.name"></v-text-field>
        </v-flex>
      </v-layout>
      <v-btn color="primary" @click="addPlayer()"> {{ addPlayerText }}</v-btn>
      <!-- <v-btn v-if="players.length < 2" disabled color="primary" @click="startGame()"> {{ textButton }}</v-btn> -->
      <v-btn color="primary" @click="startGame()"> {{ textButton }}</v-btn>
    </div>
    <v-container v-else class="background">
      <h1>Cul de Chouette Game</h1>
      <v-layout wrap>
      <v-flex
        pa-1
      >
        <v-parallax :src="require('@/assets/green.jpg')" height="1000">
          <transition name="slide-title">
            <v-layout row id="dice" justify-center justify-space-around>
              <div v-if="dices" v-for="dice in dices">
                <v-img :src="showDiceImage(dice)" height="100px" width="100px"></v-img>
              </div>
            </v-layout>
          </transition>
          <v-layout v-if="hasWinner">
            <h1>{{ winnerMsg }}</h1>
          </v-layout>
            <v-layout>
              <v-flex>
                <h1 v-if="dices.length > 0">TOTAL : {{ sumDices }}</h1>
              </v-flex>
              <v-flex>
                <h1> {{ getMove }} </h1>
              </v-flex>
            </v-layout>
        </v-parallax>
      </v-flex>
      <v-flex
        shrink
        pa-1
      >
        <v-card v-for="player in players">
          <v-card-text class="font-weight-bold display-1">{{ player.name }}</v-card-text>
          <v-card-text class="font-weight-bold"> Score : {{ player.score }}</v-card-text>
          <v-btn v-if="!hasWinner" color="primary" @click="rollDices(3, player.name)">Lancer les dès</v-btn>
        </v-card>
        <v-btn color="primary" @click="resetGame()">Reset Game</v-btn>
      </v-flex>
    </v-layout>
    </v-container>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Homepage',
  data() {
    return {
      msg: 'Bienvenue dans le Cul de Chouette!',
      textButton: "Commencer une partie",
      numberPlayersText: "Veuillez renseigner les noms des joueurs",
      addPlayerText: "Ajouter un joueur",
      players: [],
      inputs: [
        {
          label: 'Player1'
        },
        {
          label: 'Player2'
        }
      ],
      playerCreated: false,
      dices: [],
      dicesProcessing: {
        player: null,
        move: "",
        score: 0
      },
      hasWinner: false,
      winnerMsg: ""
    };
  },
  computed: {
    sumDices() {
      return this.dices.reduce((a, b) => {
        return a + b
      })
    },
    getMove() {
      return this.dicesProcessing.move ? this.dicesProcessing.move : "En attente"
    }
  },
  methods: {
    startGame() {
      const path = 'http://localhost:5000/startGame'
      axios.post(path, {
        players: this.players
      })
      .then((response) => {
        this.players = response.data
        this.playerCreated = true
      })
      .catch((err) => {
        console.error(err)
      })
    },
    addPlayer: function() {
      this.players.push({name: '', score: 0})
    },
    rollDices(numberToRolls, name) {
      const path = 'http://localhost:5000/rollDices'
      axios.post(path, {
        dices: numberToRolls
      })
      .then((response) => {
        this.dices = response.data

        if (this.dices.length == 3) {
          this.processDices(this.dices, name)
        }
      })
      .catch((err) => {
        console.error(err)
      })
    },
    processDices(dices, name) {
      this.dicesProcessing.player = name
      const path = 'http://localhost:5000/processDices'
      axios.post(path, {
        dices: dices,
        playerName: name
      })
      .then((response) => {

        if (response.data.hasWinner) {
          this.hasWinner = true
          this.winner(response.data.winner)
        }
        this.players.find((player) => {
          if (player.name == response.data.player) {
            player.score = response.data.score
          }
        })
        this.dicesProcessing = response.data
      })
      .catch((err) => {
        console.error(err)
      })
    },
    winner(name) {
      this.winnerMsg = `${name} a remporté la partie !`
    },
    resetGame() {
      const path = 'http://localhost:5000/resetGame'
      axios.get(path)
      .then((response) => {
        console.log(response)
      })
      .catch((err) => {
        console.error(err)
      })
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
