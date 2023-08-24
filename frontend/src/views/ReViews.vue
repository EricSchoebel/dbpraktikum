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
        <v-card-title>getReview:</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                "KundenID/ProduktID" (".../*" für alle Produkte), Bsp.: "baerchen76/B000024A70"
                <v-text-field v-model="input_getReview" label="Reviews für folgende Kombination aus KundenID und ggf. ProduktID" outlined></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-btn @click="submit_getReview" class="custom-green-button">Absenden</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
      
        <div v-if="output_getReview" class="output-box">
          <p class="result-heading">Ergebnis:</p> <!-- Hinzugefügt -->
          {{ output_getReview }}
        </div>
    </div>

    <br>
    <br>

    <div>
    <v-card>
      <v-card-title>addNewReview:</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_Field1"
                label="KundenID (PFLICHT)"
                outlined
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_Field2"
                label="ProduktID (PFLICHT)"
                outlined
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_Field3"
                label="Punktbewert. (PFLICHT, Ganzahl von 1 bis 5)"
                outlined
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_field4"
                label="Nützlichkeit (Ganzzahl, vzw. von 0 bis 300)"
                outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_field5"
                label="Rezensionszusammenfassung (Text)"
                outlined
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="input_field6"
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
    <div v-if="output_addNewReview" class="output-box">
      <p class="result-heading">Ergebnis:</p>
      {{ output_addNewReview }}
    </div>
  </div>

  <br>
  <br>

  <div>
      <v-card>
        <v-card-title>getTrolls:</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                mit Punkt für Dezimalzahlen, Bsp.: "4.5"
                <v-text-field v-model="input_getTrolls" label="Nutzer, deren Durchschnittsbewertung unter folgendem Wert" outlined></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-btn @click="submit_getTrolls" class="custom-green-button">Absenden</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
      
        <div v-if="output_getTrolls" class="output-box">
          <p class="result-heading">Ergebnis:</p> <!-- Hinzugefügt -->
          {{ output_getTrolls }}
        </div>
    </div>


  
  
  
  
  
  
  
  
  
  
    </main>
  
  
      
  
  
  </template>
  
  <script>
      
      
      
     /* import BarChart from "@/components/BarChart"  */
  
  
  
    export default{
  
  
    data() {
      return {
        input_getReview: '',
        output_getReview: '',
        input_Field1: "",
        input_Field2: "",
        input_Field3: "",
        input_field4: "",
        input_field5: "",
        input_field6: "",
        output_addNewReview: "",
        input_getTrolls: '',
        output_getTrolls: '',
      };
    },
  
    methods: {
      submit_getReview() {
        // Hier können Sie die Logik für die Verarbeitung der Eingabe implementieren
        // In diesem Beispiel wird die Eingabe einfach als Output angezeigt
        this.output_getReview = this.input_getReview;
                }
      ,
      submit_addNewReview() {
        // Hier können Sie die Logik für die Verarbeitung der Eingabe implementieren
        // In diesem Beispiel wird die Eingabe einfach als Output angezeigt
        this.output_addNewReview = "knopf_geht";
                }
      ,
      submit_getTrolls() {
        // Hier können Sie die Logik für die Verarbeitung der Eingabe implementieren
        // In diesem Beispiel wird die Eingabe einfach als Output angezeigt
        this.output_getTrolls = this.input_getTrolls;
                }
      ,
   
  
  
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
    font-size: 16px; /* Passen Sie die Schriftgröße an, falls erforderlich */
    font-weight: bold; /* Fettformatierung für den Text "Ergebnis" */
    margin-bottom: 5px; /* Abstand unterhalb des Textes "Ergebnis" */
  }
  
  .larger-text {
    font-size: 20px; /* Passen Sie die Schriftgröße nach Bedarf an */
  }
  
  </style>
  
  