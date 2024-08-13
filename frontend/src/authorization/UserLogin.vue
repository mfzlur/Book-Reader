<template>
  <div class="login-container">
      <div class="login-form">
          <h2>Login</h2>
          <form @submit.prevent="handleLogin">
              <label for="email">Email:</label>
              <input type="text" v-model="email" required>
              <label for="password">Password:</label>
              <input type="password" v-model="password" required>
              <br>
              <br>
              <button type="submit">Login</button>
          </form>
          <br>
          <br>
          <router-link to="/register"><p>Don't have an account!   Register Here</p></router-link>
          
      </div>
  </div>
</template>


<script>

export default {
  data() {
      return {
          email: "",
          password: "",
      };
  },
  methods: {
      handleLogin() {
          const formData = {
              email: this.email,
              password: this.password,
          };
          // console.log(this); 
          this.$axios.post("/api/login", formData)
              .then((response) => {
                  const accessToken = response.data.access_token;
                  const user_id = response.data.user_id;
                  const name = response.data.name;
                  const is_admin = response.data.is_admin;
                  localStorage.setItem("access_token", accessToken);
                  localStorage.setItem("user_id", user_id);
                  localStorage.setItem("is_admin", is_admin);
                  localStorage.setItem("name", name);
                  this.$store.commit('setAuthenticated', true);
                  this.$swal({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 2000,
                    icon: 'success',
                    title: 'Login Successful'
                  });
                  if (is_admin) {
                    this.$store.commit('setShowLibrarianNavbar', true);

                    this.$store.commit('setShowRegularNavbar', false);
                    this.$router.push('/librarian/dashboard');
                  } 
                  else { 
                    this.$store.commit('setShowRegularNavbar', true);
                    this.$store.commit('setShowLibrarianNavbar', false);
                    this.$router.push('/user/dashboard');  
                    
                  
                  }})

   
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
                  if (error.response.status === 401) {
                      this.$swal({
                        toast: true,
                        position: 'top',
                        showConfirmButton: true,
                        timer: 3000,
                        icon: 'error',
                        title: 'Unauthorized. Invalid email or password.'
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
                  
                  
              });}
  },
};
</script>



<style>
.login-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  min-height: 100vh;
  background: hwb(229 67% 28%);
}

.login-form {
  text-align: center;
  background-color: #d3eddf;
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
  color: #0056b3;
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