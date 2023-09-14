<template>
    <div></div>

    </template>
    
<script>
      export default {
        props: {
          path: String, 
        },
        data() {
          return {
            apiResult: null,
          };
        },
        watch: {
            path(newValue, oldValue) {
            if (newValue !== oldValue) {
            this.callApi(newValue);
            }
          },
        },
        methods: {
          async callApi(path) {
            try {
                const encodedPath = encodeURIComponent(path);
                const apiUrl = `http://localhost:8080/get/getProductsByCategoryPath?path=${encodedPath}`;
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
      