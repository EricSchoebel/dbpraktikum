<template>

  <main>
        <v-card rounded="0">
  
          <v-row class="ma-5">
             <v-col>
                 <h2>Kundenrezensionen</h2>
                 <v-card-text class="larger-text">Im Folgenden können Sie sich Kundenrezensionen ansehen und neue hinzufügen.
                 </v-card-text>
             </v-col>
           </v-row>
        </v-card>
  
  
  
    <div>
      <v-card>
        <v-card-title style="color: rgb(14, 14, 184);">getReview:</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                "KundenID/ProduktID" (".../*" alle Produkte zu Kunden ; "*/..." alle Kunden zu Produkt), Bsp.: "baerchen76/B000024A70"
                <v-text-field v-model="input_getReview" label="Reviews für folgende Kombination aus KundenID und ProduktID" outlined></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
           <!--     <v-btn @click="submit_getReview" class="custom-green-button">Absenden</v-btn>  -->
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
      
      <get-review 
      ref="getReview"
      :identifier="input_getReview" 
      @api-result="handle_getReview_result">
      </get-review>
  
     <div v-if="output_getReview" class="output-box" style="padding-left: 10px; padding-right: 10px;">
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">AUSGABEFORMAT PRO REZENSION:
          <br />KundenID, ProduktID, Punktbewertung, Nützlichkeit, Rezensionszusammenfassung, Rezensionsinhalt, Datum
        </p> 
        {{ output_getReview }}
      </div>
    </div>

    <br>
    <br>

    <div>
    <v-card>
      <v-card-title style="color: rgb(14, 14, 184);">addNewReview:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_addNewReview_kundenid"
                label="KundenID (PFLICHT)"
                outlined
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_addNewReview_pid"
                label="ProduktID (PFLICHT)"
                outlined
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_addNewReview_punkte"
                label="Punktbewert. (PFLICHT, Ganzahl von 1 bis 5)"
                outlined
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_addNewReview_helpful"
                label="Nützlichkeit (Ganzzahl, vzw. von 0 bis 300)"
                outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_addNewReview_summary"
                label="Rezensionszusammenfassung (Text)"
                outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_addNewReview_content"
                label="Rezensionsinhalt (Text)"
                outlined
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="6">
              <v-btn @click="submit_addNewReview" class="custom-green-button">Absenden</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>

    <add-new-review 
      ref="addNewReview"
      :kundenid="input_addNewReview_kundenid"
      :pid="input_addNewReview_pid"
      :punkte="input_addNewReview_punkte"
      :helpful="input_addNewReview_helpful"
      :summary="input_addNewReview_summary"
      :content="input_addNewReview_content"  
      :shouldSubmit="shouldSubmitAddNewReview"
      @refresherOk="handle_refresherOk"
      @refresherNotOk="handle_refresherNotOk">
    </add-new-review>
  
  </div>

  <br>
  <br>

  <div>
      <v-card>
        <v-card-title style="color: rgb(14, 14, 184);">getTrolls:</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                mit Punkt für Dezimalzahlen, Bsp.: "4.5"
                <v-text-field v-model="input_getTrolls" label="Nutzer, deren Durchschnittsbewertung unter folgendem Wert" outlined></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
             <!--      <v-btn @click="submit_getTrolls" class="custom-green-button">Absenden</v-btn> -->
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
      

      <get-trolls 
      ref="getTrolls"
      :rating="input_getTrolls" 
      @api-result="handle_getTrolls_result">
      </get-trolls>
  
     <div v-if="output_getTrolls" class="output-box" style="padding-left: 10px; padding-right: 10px;">
        <p class="result-heading">Ergebnis:</p>
        <p class="sub-heading">LISTE SOLCHER NUTZER:
        </p> 
        {{ output_getTrolls }}
      </div>


    </div>

  </main>
  
</template>
  
<script>
      
     import GetReview from "@/components/GetReview";
     import AddNewReview from "@/components/AddNewReview";
     import GetTrolls from "@/components/GetTrolls";
  
  
    export default{
    components: { // Komponenten einbinden
        GetReview,
        AddNewReview, 
        GetTrolls,
    },
    data() {
      return {
        input_getReview: '',
        output_getReview: '',
        input_addNewReview_kundenid: "",
        input_addNewReview_pid: "",
        input_addNewReview_punkte: "",
        input_addNewReview_helpful: null,
        input_addNewReview_summary: null,
        input_addNewReview_content: null,
        shouldSubmitAddNewReview: false,
        output_addNewReview: "",
        input_getTrolls: '',
        output_getTrolls: '',
      };
    },
  
    methods: {
      submit_getReview() {
        this.$refs.getReview.callApi(this.input_getReview);
      }
      ,
      handle_getReview_result(result) {
        this.output_getReview = result;
      },
      submit_addNewReview() {
        this.shouldSubmitAddNewReview = true;
        if (this.shouldSubmitAddNewReview){
          this.$refs.addNewReview.callApi(this.input_addNewReview_kundenid, this.input_addNewReview_pid, this.input_addNewReview_punkte, 
                                       this.input_addNewReview_helpful, this.input_addNewReview_summary, this.input_addNewReview_content);
        }
      },
      handle_refresherOk(result){
        if (result){
          alert('Rezension wurde gespeichert, falls ein Produkt unter dieser ProduktID vorhanden ist. Prüfen Sie Ihre Rezension über getReview.');
          window.location.reload();
        }
      },
      handle_refresherNotOk(result){
        if (result){
          alert('Ein Fehler ist aufgetreten. Beachten Sie die Eintragehinweise und versuchen Sie es erneut.');
          window.location.reload();
        }
      },
      submit_getTrolls() {
        this.$refs.getTrolls.callApi(this.input_getTrolls);
      },
      handle_getTrolls_result(result) {
        this.output_getTrolls = result;
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
  font-size: 20px; 
  font-weight: bold; /* Fettformatierung für den Text "Ergebnis" */
  margin-bottom: 5px; /* Abstand unterhalb des Textes "Ergebnis" */
}

.larger-text {
  font-size: 20px; 
}

.sub-heading {
  font-weight: bold;
  font-size: 15px;
  margin-top: 6px; /* Abstand nach oben hinzufügen */
  white-space: normal; /* Standard-Zeilenverhalten wiederherstellen */
  word-wrap: break-word; /* Zeilenumbruch bei langen Wörtern ermöglichen */
}


  
</style>
  
  