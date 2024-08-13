<template>
<div class="container">
  <div class="row">
    <div class="col">
      <h1 class="display-4 text-center">All Sections -----> <button class="btn btn-warning" @click="exportCSV">Export Data as CSV</button></h1>  
        <div class="table-responsive">
          <div v-for="section in sections" :key="section.id" class="mb-4">
            <h2 class="text-center">{{ section.name }} <button class="btn btn-info" @click="goToSection(section.id)">Go to Section</button></h2>
            <table class="table table-success table-bordered">
              <thead>
                <tr>
                  <th scope="col">Name</th>
                  <th scope="col">Author</th>
                  <th scope="col">Description</th>
                  <th scope="col">Total Copies</th>
                  <th scope="col">Copies Available</th>
                  <th scope="col">Copies Issued</th>
                  <th scope="col">Average Rating</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="book in section.books" :key="book.id">
                  <td>{{ book.name }}</td>
                  <td>{{ book.author }}</td>
                  <td>{{ book.description }}</td>
                  <td>{{ book.total_copy }}</td>
                  <td>{{ book.present_copy }}</td>
                  <td>{{ book.issued_copy }}</td>
                  <td>{{ book.average_rating }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
    </div>

  </div>

</div>


</template>

<script>

export default {
  data() {
    return {
      sections: [],
      totalBooksIssued: 0,
      totalBooksBought: 0,
      data:[],
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await this.$axios.get('/api/add/section');
        this.sections = response.data.map((section) => ({
          ...section
        }));
        console.log(this.sections)

      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    },
    goToSection(id) {
      this.$router.push({ name: 'SectionDetails', params: { id } });
    },
    async exportCSV() {
        try {
          // Sample data to send to the backend
          const data = [
            { name: 'John Doe', age: 30 },
            { name: 'Jane Smith', age: 25 }
          ];
          
  
          // Send request to start CSV generation
          const response = await this.$axios.post('http://127.0.0.1:5000/export-csv', this.sections);
  
          if (response.data.task_id) {
            const taskId = response.data.task_id;
  
            // Polling the status of the task
            const statusUrl = response.data.status_url;
            let csvUrl = null;
            while (true && csvUrl) {
              const statusResponse = await this.$axios.get(statusUrl);
              if (statusResponse.data.state === 'SUCCESS') {
                csvUrl = statusResponse.request.responseURL;
                console.log(csvUrl,statusResponse.data.state)

                // Trigger download of the generated CSV file
            const link = document.createElement('a');
            link.href = '../../../backend/export.csv';
            console.log(csvUrl)
            link.setAttribute('download', '../../../backend/export.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
                break;
              }
              console.log(statusResponse.data.state)
            }
  
            // Trigger download of the generated CSV file
            const link = document.createElement('a');
            link.href = csvUrl;
            link.setAttribute('download', './export.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
          }
        } catch (error) {
          console.error('Error exporting CSV:', error);
        }
      }

}
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
