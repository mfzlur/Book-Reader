<template>
    <div class="container">
        <h1>{{ section.name }} <button @click="editSection" class="btn btn-info">Edit Section</button> <button @click="deleteSection" class="btn btn-danger">Delete Section</button></h1>
        <p>Description: {{ section.description }}</p>
        <br>
        <button @click="toggleAllBooks">Add Books to the section</button>
        <ul><div v-show="showAllBooks">
          <li v-for="book in all_other_sec_books" :key="book.id">
            
            <h5>{{ book.name }} by {{ book.author }} <button class="btn btn-warning" @click="addBook(book.id)">Add</button></h5>
            
          </li>
        </div>
   <br>
        <h3 class="display-4">All Existing Books in this section </h3>
          <li v-for="book in section.books" :key="book.id">
            
            <h4>{{ book.name }} by {{ book.author }} <button class="btn btn-success" @click="goToBook(book.id)">Go to Book</button> <button class="btn btn-danger" @click="removeBook(book.id)">Remove </button></h4>
            
          </li>
        </ul>

        
    </div>
</template>


<script>

export default {
  data() {
    return {
      section: {},
      showAllBooks: false,
      all_other_sec_books: [],
    };
  },
  mounted() {
    this.fetchSection();
  },
  methods: {
    async fetchSection() {
      const response = await this.$axios.get(`/api/section/${this.$route.params.id}`);
      this.section = response.data;

      const response2 = await this.$axios.get(`/api/other/books/${this.$route.params.id}`);
      this.all_other_sec_books = response2.data;
    },
    editSection() {
      this.$router.push({
        name: "editSection",
        params: { id: this.$route.params.id }
      });
    },
    deleteSection() {
      this.$axios.delete(`/api/delete/section/${this.$route.params.id}`);
      this.$router.push({ name: "librarianDashboard" });
    },
    toggleAllBooks() {
      this.showAllBooks = !this.showAllBooks;
    },
    addBook(id) {
      this.$axios.post(`/api/add/book/${id}/${this.$route.params.id}`)
        .then(() => {
          this.$swal({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            icon: 'success',
            title: 'Book Added to the Section'
          });
          this.fetchSection();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    removeBook(id) {
      this.$axios.post(`/api/remove/book/${id}/${this.$route.params.id}`)
        .then(() => {
          this.$swal({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            icon: 'success',
            title: 'Book Removed from the Section'
          });
          this.fetchSection();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    goToBook(id) {
      this.$router.push({ name: "BookDetails", params: { id: id } });
    }
    
  }
};
</script>

<style scoped>
.rating {
  display: flex;
  align-items: center;
}
</style>


