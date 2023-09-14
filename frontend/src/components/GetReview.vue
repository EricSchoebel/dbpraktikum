<template>
    <div></div>

    </template>
    
<script>
      export default {
        props: {
          identifier: String, 
        },
        data() {
          return {
            apiResult: null,
          };
        },
        watch: {
            identifier(newValue, oldValue) {
            if (newValue !== oldValue) {
            this.callApi(newValue);
            }
          },
        },
        methods: {
          async callApi(identifier) {
            try {
                const encodedIdentifier = encodeURIComponent(identifier);
                const apiUrl = `http://localhost:8080/get/getReview?identifier=${encodedIdentifier}`;
                const response = await fetch(apiUrl);
    
                if (response.ok) {
                const data = await response.json();
                this.apiResult = data; 
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
      