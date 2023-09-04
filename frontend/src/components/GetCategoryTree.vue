<template>
    <div></div>
    </template>
    
<script>
      export default {
        props: {
        },
        data() {
          return {
            apiResult: null,
          };
        },
        watch: {
        },
        methods: {
          async callApi() {
            try {

                const apiUrl = `http://localhost:8080/get/getTesting`; // const apiUrl = `http://localhost:8080/get/getCategoryTree`;
                const response = await fetch(apiUrl);
    
                if (response.ok) {

                    // SO WENN ES JSON FORMAT IST:    const data = await response  ; //.json();
                    
                    //SO WENN ES KEIN JSON IST:
                    const data = await response.text();

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
      