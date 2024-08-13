<template>
    <div class="signup-container">
        <div class="signup-form">
            <h2>Edit Book</h2>
            <form @submit.prevent="editBook">
                <label for="name">Name</label>
                <input type="text" v-model="name" required>

                <label for="name">Author</label>
                <input type="text" v-model="author" required>

                <label for="name">Total Copies</label>
                <input type="number" min="1" v-model="total_copy" required>

                <label for="description">Description</label>
                <textarea id="description" rows="2" v-model="description" ></textarea>
            
                <br>
                <br>
                <button type="submit">Submit</button>
            </form>
            <br>

            
        </div>
    </div>
  </template>
  
  <script>
  
  import axios from 'axios'
  
  export default {
    data() {
        return {
              bookId: this.$route.params.id,
              name: "",
              author: "",
              total_copy: 0,
              section_id: 0,
              description: "",
    
            
        };
    },
    mounted() {
        axios.get(`/api/book/${this.bookId}`)
            .then(response => {
                this.name = response.data.name;
                this.author = response.data.author;
                this.total_copy = response.data.total_copy;
                this.section_id = response.data.section_id;
                this.description = response.data.description;
            })
            .catch(error => {
                console.error(error);
            });
    },
    methods: {
        editBook() {
            const formData = {
                name: this.name,
                author: this.author,
                total_copy: this.total_copy,
                description: this.description
            };
            axios.put(`/api/edit/book/${this.bookId}`, formData)
                .then(() => {
                    this.$swal({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 2000,
                        icon: 'success',
                        title: 'Book Edited'
                      });
                    this.$router.push({ name: 'BookDetails', params: { id: this.bookId } });
    })
                .catch((error) => {
                    console.error(error);
                });
        },
        deleteBook() {
            axios.delete(`/api/delete/book/${this.bookId}`)
                .then((response) => {
                  const msg = response.data.msg;
                    this.$swal({
                        toast: true,
                        position: 'top-end',
                        timer: 2000,
                        showConfirmButton: false,
                        icon: 'success',
                        title: msg
                      });
                      console.log(msg)
                      this.$router.push({ name: 'AllSections' });
    })
                .catch((error) => {
                    console.error(error);
                });
        }
  }}

  </script>
  <style scoped>
  .signup-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    min-height: 100vh;
    background: #acaeb7;
  }
  
  .signup-form {
    text-align: center;
    background-color: #adc4b8;
    padding: 10px;
    border-radius: 40px;
    box-shadow: 0 2px 4px rgba(178, 217, 235, 0.1);
    width: 400px;
  }
  
  h2 {
    margin-bottom: 28px;
    font-size: 32px;
    font-weight: bold;
    color: #434a47;
    
  }
  
  label {
    font-size: 14px;
    font-weight: bold;
    display: block;
    margin-bottom: 6px;
    margin-top: 12px;
    color: #3b5f85;
  }
  
  input[type="text"],
  input[type="password"],input[type="email"] {
    width: 80%;
    padding: 10px;
    margin-bottom: 12px;
    border: 1px solid #ccc;
    border-radius: 15px;
    font-size: 14px;
  }
  
  button {
    background-color: #007bff;
    color: #ffffff;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
