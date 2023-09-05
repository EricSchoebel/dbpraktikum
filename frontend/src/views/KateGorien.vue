<template>


  <main>
        <v-card rounded="0">
  
          <v-row class="ma-5">
             <v-col>
                 <h2>Kategorien</h2>
                 <v-card-text class="larger-text">Im Folgenden können Sie sich die vorhandenen Kategorien anzeigen lassen.
                 </v-card-text>
             </v-col>
           </v-row>
        </v-card>
  
  
  
    <div>
      <v-card>
        <v-card-title style="color: rgb(14, 14, 184);">getCategoryTree:</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                Achtung: es muss mit einer gewichtigen Wartezeit gerechnet werden!
              </v-col>
              <v-col cols="12" md="6">
                <v-btn @click="submit_getCategoryTree" class="custom-green-button">Abfragen</v-btn>  
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
      
      <get-category-tree 
      ref="getCategoryTree"
      @api-result="handle_getCategoryTree_result">
      </get-category-tree>
  


     <div v-if="output_getCategoryTree" class="output-box" style="padding-left: 10px; padding-right: 10px;">
         <meta charset="UTF-8"> 
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">(Einrückung für jeweilige Unterkategorie)
          <br />  
        </p> 
       <div v-html="decodeEscapedString(output_getCategoryTree)"></div>

      </div>
    </div>



    <br>
    <br>


  </main>
  
</template>




<script>
      
    import GetCategoryTree from "@/components/GetCategoryTree";
   
     export default{
      components: { // Komponenten einbinden
         GetCategoryTree,
     },
     data() {
       return {
         output_getCategoryTree: '',
      };
    },
   
    methods: {
       submit_getCategoryTree() {
         this.$refs.getCategoryTree.callApi();
       }
       ,
       handle_getCategoryTree_result(result) {
         this.output_getCategoryTree = result;
       },
       decodeEscapedString(escapedString) {
          let decodedString = escapedString
          // Ersetze andere Zeichen, die codiert sind, wie ä, ü, ö, usw.
          decodedString = decodedString.replace(/\\u([0-9a-fA-F]{4})/g, (match) => {
              return String.fromCharCode(parseInt(match.substr(2), 16));
          });  
          return decodedString;
      },
      }

       
    };
 
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
  

   

