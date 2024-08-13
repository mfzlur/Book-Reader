<template>
    <div class="home">
        <br>
        <br><br><br>
      <div @mouseover="showText" @mouseleave="hideText">
      <router-link to="/login"><img alt="app logo" src="../assets/library.png">
      <h1> Welcom to the App!! Login to continue</h1>
      <p></p></router-link> 
      <div class="hover-text" v-if="isTextVisible"> <h2>Click Anywhere to Login</h2>
        </div> 
      </div>
    </div>
  </template>
  
  <script>
  
  
  export default {
    name: 'HomeView',
    props: {
      msg: String
    },
    data() {
      return {
        isTextVisible: false
      };
    },
    methods: {
      showText() {
        this.isTextVisible = true;
      },
      hideText() {
        this.isTextVisible = false;
      }
    }
    
  }
  </script>
  
  <style scoped>
  .home {
      text-align: center;
      background-color: hwb(229 67% 28%);
      height: 100vh;
      display: flex;
      justify-content: 100%;
      align-items: center;

    
  }
  h1 {
    color: rgb(21, 88, 196);
    font-size: 40px;
    font-weight: bold;
  }
  p {
    color: white;
    font-size: 20px;
  }
  
  
  </style>