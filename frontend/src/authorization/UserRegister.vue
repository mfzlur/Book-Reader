<template>
  <div class="signup-container">
      <div class="signup-form">
          <h2>Register</h2>
          <form @submit.prevent="signup">
              <label for="name">Full Name</label>
              <input type="text" v-model="name" required>
              <label for="email">Email</label>
              <input type="email" v-model="email" required>
              <div v-if="emailError" class="error-message">{{ emailError }}</div>
              <label for="password">Password</label>
              <input type="password" v-model="password" required>
              <br>
              <br>
              <button type="submit">Register</button>
          </form>
          <br>
          <router-link to="/login"><p>Already have an account!   Login Here</p></router-link>
          
      </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  data() {
      return {
          name: "",
          password: "",
          email: "",
          emailError: "",
      
      };
  },
  methods: {
      checkEmailFormat(email) {
          const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
          return emailRegex.test(email);
      },
      signup() {
          if (!this.checkEmailFormat(this.email)) {
              this.emailError = "Invalid email format";
              return;
          }

          const formData = {
              name: this.name,
              email: this.email,
              password: this.password,
              
          };
          axios.post("/api/register", formData)
              .then(() => {
                  this.$router.push("/login");

                  this.$swal({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 2000,
                    icon: 'success',
                    title: 'Registration Successful! You can now login.'
                  });
              })
              .catch((error) => {
                  
                  if (error.request) { 
                    this.$swal({
                        toast: true,
                        position: 'top',
                        showConfirmButton: true,
                        timer: 2000,
                        icon: 'warning',
                        title: "Cannot connect to the api server. Please check your connection."
                      });
                  }
                  else if (error.response.status === 401) {
                      this.$swal({
                        toast: true,
                        position: 'top',
                        showConfirmButton: true,
                        timer: 3000,
                        icon: 'error',
                        title: error.response.data.message
                      });}
                  else {
                    this.$swal({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: true,
                        timer: 2000,
                        icon: 'error',
                        title: "Something Unexpected happend"
                      });
                  }
                  
                  
              });
             
          },

  },
};
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