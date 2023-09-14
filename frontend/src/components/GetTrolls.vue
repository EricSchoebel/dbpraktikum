<template>
    <div></div>

    </template>
    
<script>
      export default {
        props: {
          rating: Number, 
        },
        data() {
          return {
            apiResult: null,
          };
        },
        watch: {
            rating(newValue, oldValue) {
            if (newValue !== oldValue) {
            this.callApi(newValue);
            }
          },
        },
        methods: {
          async callApi(rating) {
            try {
                const encodedRating = encodeURIComponent(rating);
                const apiUrl = `http://localhost:8080/get/getTrolls?rating=${encodedRating}`;
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
      