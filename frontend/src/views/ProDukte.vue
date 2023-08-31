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
      <v-card-title style="color: rgb(14, 14, 184);">getProduct:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <!-- Ihr Textfeld oder Inhalt hier -->
              <v-text-field v-model="input_getProduct" label="Produktinfos für folgende ProduktID" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
        <!--      <v-btn @click="submit_getProduct" class="custom-green-button">Absenden</v-btn> -->
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
      <v-card-title style="color: rgb(14, 14, 184);">getProducts(String pattern):</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              SQL-Wildcards nutzen, z.B. "%" für ein oder mehr Zeichen, "_" für ein einzelnes Zeichen <!-- Ihr Textfeld oder Inhalt hier -->
              <v-text-field v-model="input_getProductsPattern" label="Produkte mit Titel mit folgendem Muster" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
        <!--       <v-btn @click="submit_getProductsPattern" class="custom-green-button">Absenden</v-btn>  -->
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
     
  
      <!-- Hier binden Sie die neue Komponente ein und übergeben die Eingabe als Eigenschaft -->
      <get-products 
      ref="getProducts"
      :pattern="input_getProductsPattern" 
      @api-result="handle_getProductsPattern_result">
      </get-products>

  
     <div v-if="output_getProductsPattern" class="output-box">
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">AUSGABEFORMAT PRO PRODUKT: ProduktID, Titel 
        </p> 
        {{ output_getProductsPattern }}
      </div>
  </div>

  <br>
  <br>

  <div>
    <v-card>
      <v-card-title style="color: rgb(14, 14, 184);">getProductsByCategoryPath:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              durch Slash getrennt, Bsp.: "Formate/Box-Sets/Blues" <!-- Hier kann man noch direkt etwas hinschreiben wenn man will -->
              <v-text-field v-model="input_getProductsByCategoryPath" label="Produkte für folgenden Kategoriepfad" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
         <!--      <v-btn @click="submit_getProductsByCategoryPath" class="custom-green-button">Absenden</v-btn> -->
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
    <get-products-by-category-path
      ref="getProductsByCategoryPath"
      :path="input_getProductsByCategoryPath" 
      @api-result="handle_getProductsByCategoryPath_result">
      </get-products-by-category-path>

  
     <div v-if="output_getProductsByCategoryPath" class="output-box">
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">AUSGABEFORMAT PRO PRODUKT: ProduktID, Titel 
        </p> 
        {{ output_getProductsByCategoryPath }}
      </div>
  </div>


  <br>
  <br>

  <div>
    <v-card>
      <v-card-title style="color: rgb(14, 14, 184);">getTopProducts:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              bei gleichem Rating Auswahl nach Titel (aufsteigend)
              <v-text-field v-model="input_getTopProducts" label="Top k Produkte für folgendes k" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
         <!--     <v-btn @click="submit_getTopProducts" class="custom-green-button">Absenden</v-btn> -->
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
      <get-top-products 
      ref="getTopProducts"
      :k="input_getTopProducts" 
      @api-result="handle_getTopProducts_result">
      </get-top-products>

  
     <div v-if="output_getTopProducts" class="output-box">
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">AUSGABEFORMAT PRO PRODUKT: ProduktID, Titel, Rating 
        </p> 
        {{ output_getTopProducts }}
      </div>



  </div>


  <br>
  <br>

  <div>
    <v-card>
      <v-card-title style="color: rgb(14, 14, 184);">getSimilarCheaperProduct:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <!-- Hier kann man noch direkt etwas hinschreiben wenn man will -->
              <v-text-field v-model="input_getSimilarCheaperProduct" label="Produkte, die ähnlich und billiger im Vergleich zu folgender ProduktID" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
        <!--      <v-btn @click="submit_getSimilarCheaperProduct" class="custom-green-button">Absenden</v-btn>  -->
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
    <get-similar-cheaper-product 
      ref="getSimilarCheaperProduct"
      :product-id="input_getSimilarCheaperProduct" 
      @api-result="handle_getSimilarCheaperProduct_result">
      </get-similar-cheaper-product>

  
     <div v-if="output_getSimilarCheaperProduct" class="output-box">
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">AUSGABEFORMAT PRO PRODUKT: ProduktID, Titel 
        </p> 
        {{ output_getSimilarCheaperProduct }}
      </div>
  </div>

  <br>
  <br>

  <div>
    <v-card>
      <v-card-title style="color: rgb(14, 14, 184);">getOffers:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <!-- Hier kann man noch direkt etwas hinschreiben wenn man will -->
              <v-text-field v-model="input_getOffers" label="Angebote für folgende ProduktID" outlined></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
       <!--       <v-btn @click="submit_getOffers" class="custom-green-button">Absenden</v-btn>  -->
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
    
    <get-offers 
      ref="getOffers"
      :product-id="input_getOffers" 
      @api-result="handle_getOffers_result">
      </get-offers>

  
     <div v-if="output_getOffers" class="output-box">
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">AUSGABEFORMAT PRO ANGEBOT:
          <br />AngebotsID, ProduktID, FilialID, Preis, Zustandsnummer, Menge, Filialname, Beschreibung
        </p> 
        {{ output_getOffers }}
      </div>

    <br>
    <br>
      

  </div>










  </main>


    


</template>

<script>
  
   import GetProduct from "@/components/GetProduct";
   import GetProducts from "@/components/GetProducts";
   import GetProductsByCategoryPath from "@/components/GetProductsByCategoryPath";
   import GetTopProducts from "@/components/GetTopProducts";
   import GetSimilarCheaperProduct from "@/components/GetSimilarCheaperProduct";
   import GetOffers from "@/components/GetOffers";


  export default{
    components: { // Komponenten einbinden
        GetProduct, 
        GetProducts,
        GetProductsByCategoryPath,
        GetTopProducts,
        GetSimilarCheaperProduct,
        GetOffers,
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
      //this.output_getProduct=this.input_getProduct;

      this.$refs.getProduct.callApi(this.input_getProduct);
    }
    ,
    handle_getProduct_result(result) {
      this.output_getProduct = result;
    },
    submit_getProductsPattern() {
      this.$refs.getProducts.callApi(this.input_getProductsPattern);
    }
    ,
    handle_getProductsPattern_result(result) {
      this.output_getProductsPattern = result;
    },
    submit_getTopProducts() {
      this.$refs.getTopProducts.callApi(this.input_getTopProducts);
    }
    ,
    handle_getTopProducts_result(result) {
      this.output_getTopProducts = result;
    },
    submit_getProductsByCategoryPath() {
      this.$refs.getProductsByCategoryPath.callApi(this.input_getProductsByCategoryPath);
    }
    ,
    handle_getProductsByCategoryPath_result(result) {
      this.output_getProductsByCategoryPath = result;
    },
    submit_getSimilarCheaperProduct() {
      this.$refs.getSimilarCheaperProduct.callApi(this.input_getSimilarCheaperProduct);
    }
    ,
    handle_getSimilarCheaperProduct_result(result) {
      this.output_getSimilarCheaperProduct = result;
    },
    submit_getOffers() {
      this.$refs.getOffers.callApi(this.input_getOffers);
    },
    handle_getOffers_result(result) {
      this.output_getOffers = result;
    },

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

