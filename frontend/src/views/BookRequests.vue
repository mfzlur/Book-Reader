<template>
    <div>
      <h1 class="display-4 text-center">Pending Requests</h1>
      <div class="text-center table-responsive" >
        <table class="table table-success table-bordered equal-width" id="data" >
          <thead class="thead dark" v-if="pending_requests.length>0">
            <tr>
              <th scope="col">Book Id</th>
              <th scope="col">User Id</th>
              <th scope="col"></th>
              <th scope="col"></th>
            </tr>
          </thead>
          <p v-else>No pending requests</p>
          <tbody>
            <tr v-for="request in pending_requests" :key="request.id">
              <td >{{ request.book_id }}</td>
              <td>{{ request.user_id }}</td>
              <td><button @click="handleRequest(request.id, 'accept')">Accept</button></td>
              <td><button @click="handleRequest(request.id, 'reject')">Reject</button></td>
            </tr>
          </tbody>
        </table>
       
      </div>
      
      <h1 class="display-4 text-center">Approved Requests</h1>
      <div class="text-center table-responsive">
        <table class="table table-success table-bordered equal-width" id="data">
          <thead class="thead dark" v-if="approved_requests.length>0">
            <tr>
              <th scope="col">Book Id</th>
              <th scope="col">User Id</th>
              <th scope="col">Approved Date</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <p v-else>No approved requests</p>
          <tbody>
            <tr v-for="request in approved_requests" :key="request.id">
              <td>{{ request.book_id }}</td>
              <td>{{ request.user_id }}</td>
              <td>{{ request.date_requested }}</td>
              <td><button @click="handleRequest(request.id, 'revoke')">Revoke</button></td>
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
        requests: [],
        pending_requests: [],
        approved_requests: [],
      };
    },
  
    created() {
      this.fetchData();
    },
  
    methods: {
      async fetchData() {
        try {
          const response = await axios.get('/api/requests'); 
          this.requests = response.data;
          this.pending_requests = this.requests.filter(request => request.status === 'pending');
          this.approved_requests = this.requests.filter(request => request.status === 'approved');
        } catch (error) {
          console.error('Failed to fetch data:', error);
        }
      },
  
      async handleRequest(id, action) {
        try {
          let response;
          if (action === 'accept') {
            response = await axios.post(`/api/accept/book/request/${id}`);
          } else if (action === 'reject') {
            response = await axios.post(`/api/reject/book/request/${id}`);
          } else if (action === 'revoke') {
            response = await axios.post(`/api/revoke/book/request/${id}`);
          }
  
          const msg = response.data.msg;
          this.$swal({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            icon: 'success',
            title: msg,
          });
  
          // Refresh the data after the request is handled
          await this.fetchData();
        } catch (error) {
          console.error('Failed to handle request:', error);
        }
      },
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
  
