

<template>
  <div id="app">
    <nav-bar />
    <router-view />

  </div>

</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavBar from "@/navbar/NavBar.vue";
</script>

<style>
body {
  font-family: sans-serif;
  margin: 0;
  padding: 0;
  background-repeat: no-repeat;
  background-size: auto;
  background: hwb(229 67% 28%);
  height: 100%; /* Ensure body takes full height */
  min-height: 100%;
  min-width: 1024px;
  width: 100%;
  align-items: center;
}

#app {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  padding-top: 60px; /* Adjust based on the navbar height */
  box-sizing: border-box;
}

nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 8;
}

router-view {
  width: 100%;
  flex-grow: 1;
}

</style>
