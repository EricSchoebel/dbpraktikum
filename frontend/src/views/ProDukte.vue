<template>

   



   





      <div>
        <v-text-field v-model="inputText" label="Eingabe" outlined></v-text-field>
        <v-btn @click="submit">Submit</v-btn>
        <div v-if="outputText">{{ outputText }}</div>
      </div>




    


</template>

<script>
    
    
    
   /* import BarChart from "@/components/BarChart"  */



    export default{


      data() {
    return {
      inputText: '',
      outputText: ''
    };
  },
  methods: {
    submit() {
      // Hier können Sie die Logik für die Verarbeitung der Eingabe implementieren
      // In diesem Beispiel wird die Eingabe einfach als Output angezeigt
      this.outputText = this.inputText;
              }
    }
    };

      /*

        components: { BarChart },
        data () {
            return {
               drawer:true,
               selectOrte: [],
               itemsOrte: [],
               selectKategorie: [],
               itemsKategorie: [],
            }
        },
        methods:{
          handleKategorie(data){
                this.itemsKategorie=data
            },
          handleOrte(data){
                this.itemsOrte=data
            },
          toggleSelectAll() {
                if (this.selectAll === true) {
                  this.selectOrte = []
                } 
                else {
                  this.selectOrte = this.itemsOrte
                }
            }, 

        }
        }
        */





   

</script>

<style>
  /*
  h2{
    text-align: center;
    position: relative;
    margin:auto;
  }
  h3{
    text-align: center;
  }
  .bar-chart-container { 
    max-width: 2000px; 
    max-height: 650px; 
    margin: 0 auto;
  }
  */
  </style>


