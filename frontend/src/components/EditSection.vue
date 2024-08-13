<template>
    <div class="signup-container">
        <div class="signup-form">
            <h2>Edit Section</h2>
            <form @submit.prevent="editSection">
                <label for="name">Name</label>
                <input type="text" v-model="section.name" required>

                <label for="description">Description</label>
                <textarea id="description" rows="2" v-model="section.description" ></textarea>
            
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
            id: this.$route.params.id,
            name: '',
            description: '',
            section: {}
    
        
        };
    },
    mounted() {
        this.fetchSection();
    },
    methods: {
        fetchSection() {
            axios.get(`/api/section/${this.id}`)
                .then((response) => {
                    this.section = response.data;
                    this.name = this.section.name;
                    this.description = this.section.description;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        editSection() {
            const formData = {
                name: this.section.name,
                description: this.section.description
            };
            axios.put(`/api/edit/section/${this.id}`, formData)
                .then(() => {
                    this.$swal({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 2000,
                        icon: 'success',
                        title: 'Section Edited'
                      });
                    this.$router.push({ name: 'SectionDetails', params: { id: this.id } });
    })
                .catch((error) => {
                    console.error(error);
                });
        },
        deleteSection() {
            axios.delete(`/api/delete/section/${this.id}`)
                .then(() => {
                    this.$swal({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 2000,
                        icon: 'success',
                        title: 'Section Deleted'
                      });
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
