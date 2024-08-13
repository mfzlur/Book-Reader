<template>
    <div class="results-container">
      <h2>Search Results for "{{ query }}"</h2>
      <ul v-if="books.length">
        <h4 class="display-4 text-info">Books</h4>
        <li v-for="book in books" :key="book.id" class="text-secondary"><h4>{{ book.name }} by {{ book.author }}</h4><button @click="viewBook(book.id)">View Book</button></li>
      </ul>
      <ul v-if="sections.length">
        <h4 class="display-4 text-info">Sections</h4>
        <li v-for="section in sections" :key="section.id" class="text-secondary"><h4>{{ section.name }} </h4><button @click="viewSection(section.id)">View Section</button></li>
      </ul>
      <h2 v-if="!books.length && !sections.length" class="text-danger">No results found.</h2>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        query: this.$route.query.q || '',
        books: [],
        sections: [],
      };
    },
    watch: {
      // Watch for changes in the query parameter and fetch data when it changes
      '$route.query.q': 'fetchResults',
    },
    mounted() {
      this.fetchResults();
    },
    methods: {
      async fetchResults() {
        try {
          const response = await axios.get(`/api/search?q=${this.query}`);
          this.books = response.data.books;
          this.sections = response.data.sections;
        } catch (error) {
          console.error('Error fetching search results:', error);
        }
      },
      viewBook(id) {
        this.$router.push({ name: 'BookDetails', params: { id } });
      },
      viewSection(id) {
        this.$router.push({ name: 'SectionDetails', params: { id } });
      },
    },

  };
  </script>
  
  <style scoped>
  .results-container {
    padding: 20px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    padding: 10px;
    border-bottom: 1px solid #ccc;
  }
  </style>
  