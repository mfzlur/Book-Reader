<template>
    <div>
      <embed :src="pdfUrl" width="200%" height="600px" type="application/pdf">
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        pdfUrl: '../public/ResumeFazlurSDE-1.pdf' // Path to your PDF file
      };
    }
  };
  </script>

  
  