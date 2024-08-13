// store/index.js

import { createStore } from 'vuex';
import axios from 'axios';
import createPersistedState from "vuex-persistedstate";

const store = createStore({
  state: {
    isAuthenticated: false,
    access_token: null,
    showRegularNavbar: true,
    showLibrarianNavbar: false,
  },
  mutations: {
    setAuthenticated(state, value) {
      state.isAuthenticated = value;
      localStorage.setItem('isAuthenticated', value);
    },
    setToken(state, token) {
      state.access_token = token; 
      localStorage.setItem('access_token', token);
    },
    setShowRegularNavbar(state, value) {
      state.showRegularNavbar = value;
    },
    setShowLibrarianNavbar(state, value) {
      state.showLibrarianNavbar = value;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('/api/login', credentials);
        commit('setAuthenticated', true);
        commit('setToken', response.data.access_token);
        localStorage.setItem('isAuthenticated', true);
      } catch (error) {
        console.error('Login failed:', error);
        throw new Error('Login failed. Please check your credentials and try again.');
      }
    },
    async logout({ commit }) {
      try {
        await axios.post('/api/logout');
        commit('setAuthenticated', false);
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('access_token');
      } catch (error) {
        console.error('Logout failed:', error);
      }
    },
  },
  plugins: [createPersistedState()]
});

const isAuthenticated = localStorage.getItem('isAuthenticated');
if (isAuthenticated) {
  store.commit('setAuthenticated', JSON.parse(isAuthenticated));
}

export default store;