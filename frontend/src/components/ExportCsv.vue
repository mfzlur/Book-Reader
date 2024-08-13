<template>
    <div>
      <button @click="exportCSV">Export Data as CSV</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    methods: {
        async exportCSV() {
        try {
          // Sample data to send to the backend
          const data = [
            { name: 'John Doe', age: 30 },
            { name: 'Jane Smith', age: 25 }
          ];
  
          // Send request to start CSV generation
          const response = await axios.post('http://127.0.0.1:5000/export-csv', data);
  
          if (response.data.task_id) {
            const taskId = response.data.task_id;
  
            // Polling the status of the task
            const statusUrl = response.data.status_url;
            let csvUrl = null;
            while (true && csvUrl) {
              const statusResponse = await axios.get(statusUrl);
              if (statusResponse.data.state === 'SUCCESS') {
                csvUrl = statusResponse.request.responseURL;
                console.log(csvUrl,statusResponse.data.state)
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
  }
  </script>
  