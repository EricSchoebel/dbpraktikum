<template>
<div></div>
   <!-- 
    <div>
      
      <div v-if="apiResult" class="output-box">
        <p class="result-heading">Ergebnis:</p>
        {{ apiResult }}
      </div>
    </div>
    -->


    

</template>
  



<script>
  export default {
    props: {
      productId: String, // Definieren Sie die Eingabe als Eigenschaft
    },
    data() {
      return {
        apiResult: null,
      };
    },
    watch: {
        productId(newValue, oldValue) {
        // Hier können Sie den API-Aufruf auslösen, wenn sich die productId ändert
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
            const apiUrl = `http://localhost:8080/get/getProduct?pid=${encodedProductId}`;
            const response = await fetch(apiUrl);

            // Überprüfen Sie, ob die Anfrage erfolgreich war (Statuscode 200)
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
  /* Stildefinitionen nach Bedarf */
  </style>
  