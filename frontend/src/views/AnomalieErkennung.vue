<template>
    <div>
      <v-navigation-drawer
        location="right"
        v-model="drawer"
        >   
  
          <v-card-title>Ortsteile auswählen:</v-card-title>
          <v-combobox
            v-model="selectOrte"
            :items="itemsOrte"
            label="Ortsteile"
            multiple
            chips
            @update:model-value="submittertwo=!submittertwo"
            :rules="[
                       v=> selectOrte.length >3 || 'mindestens 4 Ortsteile auswählen'
                   ]"
           ><template v-slot:prepend-item>
                  <v-checkbox
                    v-model="selectAll"
                    label="alle auswählen"
                    @click ="toggleSelectAll"
                    class="pl-4 mb-n6"
                  ></v-checkbox>
                  </template>
          </v-combobox>
  
          <v-card-title>Kategorien auswählen:</v-card-title>
          <v-combobox
            v-model="selectKategorie"
            :items="itemsKategorie"
            label="Kategorien"
            multiple
            chips
            @update:model-value="submittertwo=!submittertwo"
            :rules="[
                       v=> selectKategorie.length >1 || 'mindestens zwei Kategorien auswählen'
                   ]"
          ></v-combobox>

          <v-btn
          @click="submittertwo=!submittertwo"
          class="my-5 px-16"
          color="#90EE90"
          >aktualisieren</v-btn>
        <!--light orange: #FFDAB9-->
  
      </v-navigation-drawer>
    
      <main>
      
        <v-card rounded="0">
        
          <v-divider></v-divider>
          <!-- BubbleChart Diagramm -->
           <v-row class="ma-5">
             <v-col>
                 <h2>Anomalieerkennung mittels Künstlicher Intelligenz</h2>
                 <v-card-text>Im Folgenden können gegebenenfalls auftretende Ausreißer in den Daten mittels Machine Learning algorithmisch identifiziert werden.<p></p>
                  Es können Ortsteile und Kategorien gewählt werden, für erstere muss die Anzahl allerdings mindestens vier betragen. <p></p>Für den Fall von <strong>zwei Kategorien</strong> kann das Ergebnis graphisch veranschaulicht werden. Dabei können Sie über die Punkte fahren, um genauere Informationen zu erhalten.
                  Ortsteile im "Normalbereich" sind grün gefärbt, Ausreißer sind rot markiert.</v-card-text>
             </v-col>
           </v-row>
  
           <v-row class="ma-5">
             <v-col>
                <div class="bubble-chart-container" id="bubble">
               <AnomalieChart
                     ref="bChart"
                     :submittertwo="this.submittertwo"
                     :orte="this.selectOrte"
                     :kategorie="this.selectKategorie"
                     @kategorie="handleKategorie" 
                     @orte="handleOrte"
                     @annotliste="handleAnnotliste" 
                 ></AnomalieChart> 
                </div>
             </v-col>
           </v-row>

           <v-row>
          <v-col>
            <div id="gruppierungsanzeige" hidden="true">
                      <div v-for="(list, index) in this.outputliste"  :key="index">
                        <div v-if="index === 0">
                            <p style="font-weight: bold; font-size: 1.2em; margin-left: 10px; margin-right: 10px; ">Ortsteile im Normalbereich:</p>
                            <p style="margin-left: 10px; margin-right: 10px;">{{ list.join(', ') }}</p>
                            <br>
                        </div>
                        <div v-if="index === 1">
                            <p style="font-weight: bold; font-size: 1.2em; margin-left: 10px; margin-right: 10px;">Ausreißer:</p>
                            <p style="margin-left: 10px; margin-right: 10px;">{{ list.join(', ') }}</p>
                        </div>
                      </div>
            </div>
          </v-col>
         </v-row>
  
  
        </v-card>
      </main>
  
    </div>
  </template>
  
  <script>
  import AnomalieChart from "@/components/AnomalieChart";
  //import TestZwei from "@/components/TestZwei";
  export default {
    components: { AnomalieChart },
    data(){
      return{
        drawer:true,
        selectOrte: [],
        itemsOrte: [],
        selectKategorie: [],
        itemsKategorie: [],
        vielDimensional: false,
        annotListe: [],
        submittertwo: false,
        outputliste: [[],[]],
      }
    },
    methods:{
      handleKategorie(data){
                    this.itemsKategorie=data
              },
      handleOrte(data){
                  this.itemsOrte=data
              },
      handleAnnotliste(data){
                this.annotListe=data
            },
      toggleSelectAll() {
      if (this.selectAll === true) {
        this.selectOrte = []
      } 
      else {
        this.selectOrte = this.itemsOrte
      }
              },
      async processLists(list1, list2) { //list1 ist annotliste , list2 ist SelectOrtsteile, Output ist Liste von Listen
        /* Bsp.:
        let list1 = [0, 0, 1, 2];
        let list2 = ["A", "B", "C", "D"];
        let listOutput = processLists(list1, list2);
        console.log(listOutput);   ->  [["A", "B"], ["C"], ["D"]]
           -> die stelle der liste sagt list1, was darein kommt sagt list2
        */
        let result = [];
        
        for (let i = 0; i < list1.length; i++) {
          let value = list1[i];
          let element = list2[i];
          
          if (!result[value]) {
            result[value] = [];
          }
          
          result[value].push(element);
        }
        
        this.outputliste=result.filter(Boolean);
    },
    
  
    },
    watch:{
      selectKategorie(val){
      if (val.length>2){
        this.vielDimensional = true
        this.processLists(this.annotListe, this.selectOrte)
        console.log("unser list von lits outputliste")
        console.log(this.outputliste)
      }
      else{
        this.vielDimensional = false
        this.processLists(this.annotListe, this.selectOrte)
        console.log("unser list von lits outputliste")
        console.log(this.outputliste)
      }
    },
    vielDimensional(val){
      if (val===true){
        document.getElementById("bubble").hidden = true
        document.getElementById("gruppierungsanzeige").hidden = false
        this.processLists(this.annotListe, this.selectOrte)
        console.log("unser list von lits outputliste")
        console.log(this.outputliste)
      }
      else{
        document.getElementById("bubble").hidden = false
        document.getElementById("gruppierungsanzeige").hidden = true
        this.processLists(this.annotListe, this.selectOrte)
        console.log("unser list von lits outputliste")
        console.log(this.outputliste)
      }
    },
    selectOrte(){
      this.processLists(this.annotListe, this.selectOrte)
      console.log("unser list von lits outputliste")
      console.log(this.outputliste)
    },
    submittertwo(){
      this.processLists(this.annotListe, this.selectOrte)
      console.log("unser list von lits outputliste")
      console.log(this.outputliste)
    },
    
    },
   
  }
  </script>
  <style>
  h2{
    text-align: center;
    position: relative;
    margin:auto;
  }
  h3{
    text-align: center;
  }
  .bubble-chart-container {
    max-width: 800px; 
    max-height: 600px; 
    margin: 0 auto; /* Center the chart horizontally */ 
  }
  </style>