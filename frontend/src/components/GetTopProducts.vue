<template>
    <div></div>

</template>
    
<script>
      export default {
        props: {
          k: Number, 
        },
        data() {
          return {
            apiResult: null,
          };
        },
        watch: {
            k(newValue, oldValue) {
            if (newValue !== oldValue) {
            this.callApi(newValue);
            }
          },
        },
        methods: {
          async callApi(k) {
            try {
                const encodedPattern = encodeURIComponent(k);
                const apiUrl = `http://localhost:8080/get/getTopProducts?k=${encodedPattern}`;
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
      