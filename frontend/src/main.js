import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import axios from 'axios'

import store from './store'; 


import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';




const app = createApp(App)


// global configuration for axios
app.config.globalProperties.$axios = axios

//default base url configuration for axios
axios.defaults.baseURL='http://127.0.0.1:5000'



axios.interceptors.request.use(
    (config) => {
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        config.headers['Authorization'] = `Bearer ${accessToken}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

app.use(router)
app.use(VueSweetalert2)
app.use(store)


app.mount('#app')
