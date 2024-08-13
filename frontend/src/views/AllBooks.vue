<template>
    <div>
      <h1 class="display-4 text-center">All Books</h1>
      <div class="text-center table-responsive">
          
          <table class="table table-success table-bordered equal-width" id="data">
            <thead class="thead dark">
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Author</th>
                <th scope="col">Description</th>
                <th scope="col">Average Rating</th>
                <th scope="col">Section Name</th>
                <th scope="col"></th>
                <th scope="col"></th>
              </tr>
            </thead>
            <tbody >
              <tr v-for="book in books" :key="book.id">
                <td>{{ book.name }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.description }}</td>
                <td>{{ book.average_rating }}</td>
                <td>{{ book.section }}</td>
                <td>
                <div class="dropdown">
                <button @click="toggle" type="button" class="btn btn-primary">Rate Book</button>
                <div v-show="showDropdown">
                  <button @click="selectRating(book.id, 1)">1</button>
                  <button @click="selectRating(book.id, 2)">2</button>
                  <button @click="selectRating(book.id, 3)">3</button>
                  <button @click="selectRating(book.id, 4)">4</button>
                  <button @click="selectRating(book.id, 5)">5</button>
                </div>
              </div></td>
                <td><button @click="requestBook(book.id)" class="btn btn-info">{{ request_status}}</button></td>

              </tr>
            </tbody>
          </table>
        </div>
      </div>
</template>

<script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        books: [],
        showDropdown: false,
        request_status: "Request Book"
      };
    },
    created() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          const response = await axios.get('/api/add/book'); // Update with your API endpoint
          this.books = response.data.map((book) => ({
            ...book}));
        } catch (error) {
          console.error('Failed to fetch data:', error);
        }
      },
      toggle() {
        this.showDropdown = !this.showDropdown;
      },
      selectRating(id, rating) {
        axios.post(`/api/add/book/rating/${id}`, { rating })
        .then((response) => {
          const msg = response.data.msg;
              this.$swal({
                  toast: true,
                  position: 'top-end',
                  showConfirmButton: false,
                  timer: 3000,
                  icon: 'success',
                  title: msg
                })});
        this.fetchData();
        this.showDropdown = false;
      },
      requestBook(id) {
        axios.post(`/api/book/request/${id}`)
        .then((response) => {
          const msg = response.data.msg;
              this.$swal({
                  toast: true,
                  position: 'top-end',
                  showConfirmButton: false,
                  timer: 3000,
                  icon: 'success',
                  title: msg
                })});
        this.fetchData();

      }
    },
  };
  </script>
  
  <style scoped>
  .text-center {
    text-align: center;
  }
  .table-responsive {
    overflow-x: auto;
  }
 
  </style>

