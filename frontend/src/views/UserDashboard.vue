<template>
    <div class="container my-5">
  
      <h1 class="display-4 text-center">Welcome {{ name }}</h1> <br>
      <h2 class="text-center">Here are some statistics</h2>

      <br>
      <br>
      <h2 class="display-4">Total Books Issued Now: {{ totalBooksIssued }}</h2>
      <h2 class="display-4">Total Books Pending Now: {{ totalBooksPending }}</h2>
      <h2 class="display-4">Total Books Bought : {{ totalBooksBought }}</h2>
      <p class="display-4">Visit My Books section for more details</p>
      
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        totalBooksIssued: 0,
        totalBooksBought: 0,
        name: localStorage.getItem('name'),
        totalBooksPending: 0,
      };
    },
    created() {
      this.fetchUserProfile();
    },
    methods: {
      async fetchUserProfile() {
        try {
          const response = await axios.get('/api/user/profile'); 
          this.totalBooksIssued = response.data.total_issued_books;
          this.totalBooksBought = response.data.total_bought_books;
          this.totalBooksPending = response.data.total_pending_books;
        } catch (error) {
          console.error('Failed to fetch user profile:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .text-center {
    text-align: center;
  }
  
  .img-rounded {
    border-radius: 50%;
  }
  
  .img-thumbnail {
    padding: 0.25rem;
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 0.25rem;
    max-width: 100%;
    height: auto;
  }
  </style>
  