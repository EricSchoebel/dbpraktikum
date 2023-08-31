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
                // Führen Sie hier Ihren API-Aufruf durch und speichern Sie das Ergebnis in apiResult
                // Beispiel:
                const encodedProductId = encodeURIComponent(productId);
                const apiUrl = `http://localhost:8080/get/getSimilarCheaperProduct?pid=${encodedProductId}`;
                const response = await fetch(apiUrl);
    
                // Überprüfen Sie, ob die Anfrage erfolgreich war (Statuscode 200)
                if (response.ok) {
                const data = await response.json();
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
      </style>
      