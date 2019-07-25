import Vue from 'vue';
import Router from 'vue-router';
import Homepage from './views/Homepage.vue';
import Board from './views/Board.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Homepage',
      component: Homepage,
    },
    {
      path: '/startGame',
      name: 'Board',
      component: Board,
    },
  ],
});
