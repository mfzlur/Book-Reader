<template>
  <div class="container">
      <h1>{{ book.name }} <button @click="editBook" class="btn btn-info">Edit Book</button> <button @click="deleteBook" class="btn btn-danger">Delete Book</button></h1>
      <h4>Author: {{ book.author }}</h4>
      <h4>Description: {{ book.description }}</h4>
      <h4>Total Copies: {{ book.total_copy }}</h4>
      <h4>Present Copies: {{ book.present_copy }}</h4>
      <h4>Issued Copies: {{ book.issued_copy }}</h4>
      <h4>Avg Rating: {{ book.average_rating }}</h4>
      <h4>Section: {{ book.section }} <button class="btn btn-success" @click="goToSection(book.section_id)">Go to Section</button> </h4>
      <br>
      <ul>
 <br>
      
      </ul>

      
  </div>
</template>


<script>

export default {
data() {
  return {
    book: {},
    showAllSections: false,

  };
},
mounted() {
  this.fetchBook();
},
methods: {
  async fetchBook() {
    const response = await this.$axios.get(`/api/book/${this.$route.params.id}`);
    this.book = response.data;

  },
  editBook() {
    this.$router.push({
      name: "editBook",
      params: { id: this.$route.params.id }
    });
  },
  deleteBook() {
    this.$axios.delete(`/api/delete/book/${this.$route.params.id}`);
    this.$router.push({ name: "librarianDashboard" });
  },
  
  
  goToSection(id) {
    this.$router.push({ name: "SectionDetails", params: { id: id } });
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

