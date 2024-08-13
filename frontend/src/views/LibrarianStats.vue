<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <div class="row">
                    <div class="col">
                        <div class="card text-white bg-dark mb-3" style="max-width: 18rem;">
                            <div class="card-header fs-2">Total Books</div>
                            <div class="card-body">
                                <h5 class="card-title fs-2">{{ total_books }}</h5>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card text-white bg-dark mb-3" style="max-width: 18rem;">
                            <div class="card-header fs-2">Total Sections</div>
                            <div class="card-body">
                                <h5 class="card-title fs-2">{{ total_sections }}</h5>
                            </div>
                        </div>
                    </div>
                    <div class="w-100"></div>
                    <div class="col">
                        <div class="card text-white bg-dark mb-3" style="max-width: 18rem;">
                            <div class="card-header fs-2">Total Books Issued</div>
                            <div class="card-body">
                                <h5 class="card-title fs-2">{{ total_books_issued }}</h5>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card text-white bg-dark mb-3" style="max-width: 18rem;">
                            <div class="card-header fs-2">Total Books Bought</div>
                            <div class="card-body">
                                <h5 class="card-title fs-2">{{ total_books_bought }}</h5>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col"> <br><br><br><br><Bar v-if="loaded" :data="chartData" /></div>
            <div class="w-100"></div>
            <div class="col">
                <div class="row">
                    <div class="col">
                        <div class="card text-white bg-dark mb-3" style="max-width: 18rem;">
                            <div class="card-header fs-2">Total Users</div>
                            <div class="card-body">
                                <h5 class="card-title fs-2">{{ total_users }}</h5>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card text-white bg-dark mb-3" style="max-width: 18rem;">
                            <div class="card-header fs-2">Average Book Rating</div>
                            <div class="card-body">
                                <h5 class="card-title fs-2">{{ average_book_rating }}</h5>
                            </div>
                        </div>
                    </div>
                    <div class="w-100"></div>

                </div>
            </div>
            <div class="col"></div>
        </div>
    </div>


</template>

<script>

import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
export default {
    name: 'BarChart',
    components: { Bar },
    data() {
        return {
            total_books:0,
            total_sections:0,
            total_books_issued:0,
            total_books_bought:0,
            total_users:0,
            average_book_rating:0,
            loaded: false,
            chartData: null
        }
    }
    ,
    async mounted() {
        this.loaded = false
  
  try {
    const response = await this.$axios.get('/api/chartdata')
    console.log(response.data.labels)
    console.log(response.data.data)
    this.chartData = {
      labels: response.data.labels,
      datasets: [
        {
          label: 'No of books per section',
          data: response.data.data,
          backgroundColor: 'rgba(75, 9, 192, 0.2)',
          borderColor: 'rgba(75, 192, 0, 1)',
          borderWidth: 0.5
        }
      ]
    }

    this.loaded = true
    const response2 = await this.$axios.get('/api/librarian/stats');
        this.total_books = response2.data.total_books;
        this.total_sections = response2.data.total_sections;
        this.total_books_issued = response2.data.total_books_issued;
        this.total_books_bought = response2.data.total_books_bought;
        this.total_users = response2.data.total_users;
        this.average_book_rating = response2.data.average_book_rating;
  } catch (e) {
    console.error(e)
  }

    },

}
</script>

