<template>
    <div class="container">
      <Pie v-if="loaded" :data="chartData" />
    </div>
  </template>
  
  <script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)
  
  export default {
    name: 'PieChart',
    components: { Pie },
    data: () => ({
      loaded: false,
      chartData: null
    }),
    async mounted () {
      this.loaded = false
  
      try {
        const response = await this.$axios.get('/api/chartdata')
        console.log(response.data.labels)
        console.log(response.data.data)
        this.chartData = {
          labels: response.data.labels,
          datasets: [
            {
              label: 'Sales',
              data: response.data.data,
              backgroundColor: 'rgba(75, 9, 192, 0.2)',
              borderColor: 'rgba(75, 192, 0, 1)',
              borderWidth: 0.5
            }
          ]
        }
  
        this.loaded = true
      } catch (e) {
        console.error(e)
      }
    }
  }
  </script>

