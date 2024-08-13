<template>
  <div>
    <h1 class="display-4 text-center">Approved or Pending Books</h1>
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
            <th scope="col">Status</th>
            <th scope="col"></th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in approved_books" :key="book.id">
            <td>{{ book.name }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.description }}</td>
            <td>{{ book.average_rating }}</td>
            <td>{{ book.section }}</td>
            <td>
              <div class="dropdown">
                <button @click="toggle" type="button" class="btn btn-secondary">Rate Book</button>
                <div v-show="showDropdown">
                  <button @click="selectRating(book.id, 1)">1</button>
                  <button @click="selectRating(book.id, 2)">2</button>
                  <button @click="selectRating(book.id, 3)">3</button>
                  <button @click="selectRating(book.id, 4)">4</button>
                  <button @click="selectRating(book.id, 5)">5</button>
                </div>
              </div>
            </td>
            <td><button>{{ book.request_status }}</button></td>
            <td v-show="book.request_status == 'approved'"><button class="btn btn-success"
                @click="buyBook(book.id)">Buy</button></td>
            <td v-show="book.request_status == 'approved'"><button class="btn btn-info"
                @click="returnBook(book.id)">Return</button></td>
            <td v-show="book.request_status == 'approved'"><button class="btn btn-warning"
                @click="openPdf(book.filename)">{{ showPdf ? 'Hide Pdf' : 'Show Pdf' }}</button></td>

          </tr>
        </tbody>
      </table>

    </div>
    <div v-show="showPdf" class="text-center">
              <embed :src="pdfUrl" width="75%" height="1100px" type="application/pdf">
            </div>


    <h1 class="display-4 text-center">Bought Books</h1>
    <div class="text-center table-responsive">

      <table class="table table-success table-bordered equal-width" id="data">
        <thead class="thead dark">
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Author</th>
            <th scope="col">Average Rating</th>
            <th scope="col">Quantity</th>
            <th scope="col"></th>

          </tr>
        </thead>
        <tbody>
          <tr v-for="book in bought_books" :key="book.id">
            <td>{{ book.book_name }}</td>
            <td>{{ book.book_author }}</td>
            <td>{{ book.average_rating }}</td>
            <td>{{ book.quantity }}</td>
            <td><button @click="downloadFile(book.filename)" type="button" class="btn btn-success">Download Pdf</button>
            </td>


          </tr>
        </tbody>
      </table>
    </div>

    <h1 class="display-4 text-center">Returned or Rejected Books</h1>
    <div class="text-center table-responsive">

      <table class="table table-success table-bordered equal-width" id="data">
        <thead class="thead dark">
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Author</th>
            <th scope="col">Average Rating</th>
            <th scope="col">Request Status</th>


          </tr>
        </thead>
        <tbody>
          <tr v-for="book in returned_books" :key="book.id">
            <td>{{ book.name }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.average_rating }}</td>
            <td>{{ book.request_status }}</td>



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
      bought_books: [],
      returned_books: [],
      approved_books: [],
      pdfUrl: '',
      view_status: 'View Book',
      showPdf: false,
      
  
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('/api/my/books');// Update with your API endpoint
        this.books = response.data.map((book) => ({
          ...book
        }));
        this.returned_books = this.books.filter(book => book.request_status === 'rejected' || book.request_status === 'returned');
        this.approved_books = this.books.filter(book => book.request_status === 'approved' || book.request_status === 'pending');
        console.log(this.returned_books);
        const response2 = await axios.get('/api/bought/books');
        this.bought_books = response2.data.map((book) => ({
          ...book
        }))
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
          })
        });
      this.fetchData();
      this.showDropdown = false;
    },

    buyBook(id) {
      this.$swal({
        title: 'Please make virtual Payment to buy the book',
        text: "You can click on Yes, to confirm",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, buy the book!'
      }).then((result) => {
        if (result.isConfirmed) {
          axios.post(`/api/buy/book/${id}`)
            .then((response) => {
              const msg = response.data.msg;
              this.$swal({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                icon: 'success',
                title: msg
              })
            });
          this.fetchData();
        }
      })

    },

    returnBook(id) {
      axios.post(`/api/return/book/${id}`)
        .then((response) => {
          this.fetchData();
          const msg = response.data.msg;
          this.$swal({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            icon: 'success',
            title: msg
          })
        });


    },


    async downloadFile(filename) {
      // if (!filename) return;

      try {
        const response = await axios.get(`/download/${filename}`, {
          responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error("There was an error downloading the file:", error);
        alert("File download failed.");
      }
    },
    openPdf(filename) {
      this.showPdf = !this.showPdf;
      this.pdfUrl = `../public/${filename}`;
      console.log(this.pdfUrl);
      this.view_status = 'Hide Book';
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
