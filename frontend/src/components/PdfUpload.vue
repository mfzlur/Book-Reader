<template>
    <div class="container">
      <h1 class="display-4 text-center">Upload and Download PDF</h1>
      <form @submit.prevent="uploadFile" class="text-center">
        <div class="form-group">
          <label for="file">Choose a PDF file to upload:</label>
          <input type="file" id="file" @change="handleFileUpload" accept="application/pdf">
        </div>
        <button type="submit" class="btn btn-primary">Upload PDF</button>
      </form>
  
      <div v-if="uploadedFilename" class="text-center mt-4">
        <button @click="downloadFile" class="btn btn-success">Download PDF</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        file: null,
        uploadedFilename: null,
      };
    },
    methods: {
      handleFileUpload(event) {
        this.file = event.target.files[0];
      },
      async uploadFile() {
        if (!this.file) {
          alert("Please select a file first.");
          return;
        }
  
        let formData = new FormData();
        formData.append('file', this.file);
  
        try {
          const response = await axios.post('/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          this.uploadedFilename = response.data.filename;
          alert("File uploaded successfully.");
        } catch (error) {
          console.error("There was an error uploading the file:", error);
          alert("File upload failed.");
        }
      },
      async downloadFile() {
        if (!this.uploadedFilename) return;
  
        try {
          const response = await axios.get(`/download/${this.uploadedFilename}`, {
            responseType: 'blob',
          });
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', this.uploadedFilename);
          document.body.appendChild(link);
          link.click();
          link.remove();
        } catch (error) {
          console.error("There was an error downloading the file:", error);
          alert("File download failed.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: 50px auto;
  }
  </style>
  