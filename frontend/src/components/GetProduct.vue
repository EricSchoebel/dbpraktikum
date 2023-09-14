<template>
<div></div>
  

</template>
  



<script>
  export default {
    props: {
      productId: String, 
    },
    data() {
      return {
        apiResult: null,
      };
    },
    watch: {
        productId(newValue, oldValue) {
        if (newValue !== oldValue) {
        this.callApi(newValue);
        }
      },
    },
    methods: {
      async callApi(productId) {
        try {
            const encodedProductId = encodeURIComponent(productId);
            const apiUrl = `http://localhost:8080/get/getProduct?pid=${encodedProductId}`;
            const response = await fetch(apiUrl);

            if (response.ok) {
            const data = await response.text();
            this.apiResult = data; // Das Ergebnis in apiResult speichern
            // Senden Sie das Ergebnis an die übergeordnete Ansicht
            this.$emit('api-result', this.apiResult);
            } else {
            console.error('Fehler bei der API-Anfrage:', response.statusText);
            }

        } catch (error) {
          console.error('Fehler bei der API-Anfrage:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* --- */
  </style>
  