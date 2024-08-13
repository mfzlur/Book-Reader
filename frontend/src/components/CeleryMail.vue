<template>
    <div>
      <h1 class="text-secondary">Send Mail Using Celery</h1>
      <label for="name">Recipient Name</label>
      <input type="text" id="name" v-model="name" required>
      <br>
      <label for="email">Recipient Email</label>
      <input type="email" id="email" v-model="email" required>
      <br>
      <button @click="sendRequest">Send Email</button>
      <p class="fs-1 text-dark">{{ output }}</p> 
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'CeleryMail',
    data() {
      return {
        output: '',
        name: '',
        email: '',
    
      };
    },
    methods: {
      async sendRequest() {
        const response = await this.$axios.post(`/api/celery/email/${this.name}/${this.email}`);
        console.log(response.data);
        const task_id = response.data.task_id;
  
        let status = null;
        const intervalId = setInterval(async () => {
          const response2 = await this.$axios.get(`/api/celery/email/status/${task_id}`);
          status = response2.data.status;
          if (status === 'SUCCESS') {
            const result = response2.data.result;
            this.output = result;
            clearInterval(intervalId);
          }
          else{
              this.output = 'Hang On Email is on the way...';
              console.log(this.output);
          }
        }, 2000);
        
        
      },
      
    }
  }
  </script>