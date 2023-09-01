<template>
    <div></div>
</template>
    
<script>
      export default {
        props: {
          kundenid: String, 
          pid: String, 
          punkte: Number,
          helpful: Number,
          summary: String,
          content: String,
          shouldSubmit: Boolean
        },
        data() {
          return {
            apiResult: null,
          };
        },
        watch: {
            shouldSubmit(newShouldSubmit, oldShouldSubmit) {
                if (newShouldSubmit && !oldShouldSubmit) { // Überwachen der shouldSubmit-Flagge
                    if (this.kundenid != null && this.pid != null && this.punkte != null){
                        this.callApi(kundenid, pid, punkte, helpful, summary, content); // Wenn die Flagge true wird, API-Call
                    }
                }
            },
        },
        methods: {
          async callApi(kundenid, pid, punkte, helpful, summary, content) {
            try {
                const apiUrl = 'http://localhost:8080/post/addNewReview';
                const requestBody = {
                    kundenid,
                    pid,
                    punkte,
                    helpful,
                    summary,
                    content,
                };

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestBody),
                });

                if (response.ok){
                    this.$emit('refresherOk', true);
                }
                else {
                    this.$emit('refresherNotOk', true)
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
      


