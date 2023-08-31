<template>

   



   



<main>
      <v-card rounded="0">

        <v-row class="ma-5">
           <v-col>
               <h2>Produkte</h2>
               <v-card-text class="larger-text">Im Folgenden können Sie sich Informationen zu den Produkten aus der Datenbank anzeigen lassen.
               </v-card-text>
           </v-col>
         </v-row>
      </v-card>




  <div>
    <v-card>
      <v-card-title>getProduct:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <!-- Ihr Textfeld oder Inhalt hier -->
              <v-text-field v-model="input_getProduct" label="Produktinfos für folgende ProduktID" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-btn @click="submit_getProduct" class="custom-green-button">Absenden</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
    <!-- Hier binden Sie die neue Komponente ein und übergeben die Eingabe als Eigenschaft -->
    <get-product 
    ref="getProduct"
    :product-id="input_getProduct" 
    @api-result="handle_getProduct_result">
    </get-product>

  </div>
     <div v-if="output_getProduct" class="output-box">
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">AUSGABEFORMAT: ProduktID, Titel, Rating, Verkaufsrang,
           <br />(falls Buch:) Seitenzahl, Erscheinungsdatum, ISBN, Verlag,
           <br />(falls DVD:) Format, Laufzeit, Regioncode
           <br />(falls CD:) Label, Erscheinungsdatum
        </p> 
        {{ output_getProduct }}
    </div>
  


  <br>
  <br>

  <div>
    <v-card>
      <v-card-title>getProducts(String pattern):</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <!-- Ihr Textfeld oder Inhalt hier -->
              <v-text-field v-model="input_getProductsPattern" label="Produkte mit Titel mit folgendem Muster" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-btn @click="submit_getProductsPattern" class="custom-green-button">Absenden</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
    <div v-if="output_getProductsPattern" class="output-box">
        <p class="result-heading">Ergebnis:</p><!-- Hinzugefügt -->
        <p class="sub-heading">Unterüberschrift hier, oerer, gauki, dfhdiulfqiwefrew, feruifrewfr</p> 
        {{ output_getProductsPattern }}
    </div>
  </div>


  <br>
  <br>

  <div>
    <v-card>
      <v-card-title>getTopProducts:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <!-- Hier kann man noch direkt etwas hinschreiben wenn man will -->
              <v-text-field v-model="input_getTopProducts" label="Top k Produkte für folgendes k" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-btn @click="submit_getTopProducts" class="custom-green-button">Absenden</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
      <div v-if="output_getTopProducts" class="output-box">
        <p class="result-heading">Ergebnis:</p> <!-- Hinzugefügt -->
        {{ output_getTopProducts }}
      </div>
  </div>

  <br>
  <br>

  <div>
    <v-card>
      <v-card-title>getProductsByCategoryPath:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              durch Slash getrennt, Bsp.: "Formate/Box-Sets/Blues" <!-- Hier kann man noch direkt etwas hinschreiben wenn man will -->
              <v-text-field v-model="input_getProductsByCategoryPath" label="Produkte für folgenden Kategoriepfad" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-btn @click="submit_getProductsByCategoryPath" class="custom-green-button">Absenden</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
      <div v-if="output_getProductsByCategoryPath" class="output-box">
        <p class="result-heading">Ergebnis:</p> <!-- Hinzugefügt -->
        {{ output_getProductsByCategoryPath }}
      </div>
  </div>

  <br>
  <br>

  <div>
    <v-card>
      <v-card-title>getSimilarCheaperProduct:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <!-- Hier kann man noch direkt etwas hinschreiben wenn man will -->
              <v-text-field v-model="input_getSimilarCheaperProduct" label="Produkte, die ähnlich und billiger im Vergleich zu folgender ProduktID" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-btn @click="submit_getSimilarCheaperProduct" class="custom-green-button">Absenden</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
      <div v-if="output_getSimilarCheaperProduct" class="output-box">
        <p class="result-heading">Ergebnis:</p> <!-- Hinzugefügt -->
        {{ output_getSimilarCheaperProduct }}
      </div>
  </div>

  <br>
  <br>

  <div>
    <v-card>
      <v-card-title>getOffers:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <!-- Hier kann man noch direkt etwas hinschreiben wenn man will -->
              <v-text-field v-model="input_getOffers" label="Angebote für folgende ProduktID" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-btn @click="submit_getOffers" class="custom-green-button">Absenden</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
      <div v-if="output_getOffers" class="output-box">
        <p class="result-heading">Ergebnis:</p> <!-- Hinzugefügt -->
        {{ output_getOffers }}
      </div>
  </div>










  </main>


    


</template>

<script>
    
    
    
   /* import BarChart from "@/components/BarChart"  */
   import GetProduct from "@/components/GetProduct";


  export default{
    components: {
        GetProduct, // Komponente einbinden
  },

  data() {
    return {
      input_getProduct: '',
      output_getProduct: '',
      input_getProductsPattern: '',
      output_getProductsPattern: '',
      input_getTopProducts: '',
      output_getTopProducts: '',
      input_getProductsByCategoryPath: '',
      output_getProductsByCategoryPath: '',
      input_getSimilarCheaperProduct: '',
      output_getSimilarCheaperProduct: '',
      input_getOffers: '',
      output_getOffers: '',
    };
  },

  methods: {
    submit_getProduct() {
      // Hier können Sie die Logik für die Verarbeitung der Eingabe implementieren
      // In diesem Beispiel wird die Eingabe einfach als Output angezeigt

      // Die Eingabe wird an die neue Komponente übergeben, wenn der "Absenden"-Button geklickt wird
      // Das Ergebnis wird über die Methode handle_getProduct_result empfangen
      
      //TEST:
      this.output_getProduct=this.input_getProduct;

      //this.$refs.getProduct.callApi(this.input_getProduct);
              }
    ,
    handle_getProduct_result(result) {
      this.output_getProduct = result;
    },
    submit_getProductsPattern() {
      this.output_getProductsPattern = this.input_getProductsPattern;
              }
    ,
    submit_getTopProducts() {
      this.output_getTopProducts = this.input_getTopProducts;
              }
    ,
    submit_getProductsByCategoryPath() {
      this.output_getProductsByCategoryPath = this.input_getProductsByCategoryPath;
              }
    ,
    submit_getSimilarCheaperProduct() {
      this.output_getSimilarCheaperProduct = this.input_getSimilarCheaperProduct;
              }
    ,
    submit_getOffers() {
      this.output_getOffers = this.input_getOffers;
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

<style scoped>
.custom-green-button {
  background-color: green;
  color: white;
  margin-top: 10px;
}

.output-box {
  margin-left: 20px;
}

.result-heading {
  font-size: 20px; /* Passen Sie die Schriftgröße an, falls erforderlich */
  font-weight: bold; /* Fettformatierung für den Text "Ergebnis" */
  margin-bottom: 5px; /* Abstand unterhalb des Textes "Ergebnis" */
}

.larger-text {
  font-size: 20px; /* Passen Sie die Schriftgröße nach Bedarf an */
}

.sub-heading {
  font-weight: bold;
  font-size: 15px;
  margin-top: 6px; /* Abstand nach oben hinzufügen */
  white-space: normal; /* Standard-Zeilenverhalten wiederherstellen */
  word-wrap: break-word; /* Zeilenumbruch bei langen Wörtern ermöglichen */
}



</style>

