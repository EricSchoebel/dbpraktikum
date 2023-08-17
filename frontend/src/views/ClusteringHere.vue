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
          >
                  <template v-slot:prepend-item>
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
          :rules="[
                       v=> selectKategorie.length >1 || 'mindestens zwei Kategorien auswählen'
                   ]"
          
        ></v-combobox>

        <v-card-title>Clusteranzahl</v-card-title>
        <v-text-field
                   v-model="anzahl"
                   :rules="[
                       v=> v>0 || 'Anzahl muss größer 0 sein'
                   ]"
                   label="Anzahl"
                   variant="outlined"
                   class="px-5 pb-3"
                   type="number"
                   :disabled="optimierer"
                   @update:model-value="submitter=!submitter"
        ></v-text-field>
        
        <v-checkbox
          v-model="optimierer"
          class="my-n8 px-3"
          label="optimieren lassen"
          @change="test=!test"
        ></v-checkbox>
        
        <v-btn
         @click="submitter=!submitter"
         class="my-5 px-16"
         color="#90EE90"
        >aktualisieren</v-btn>
        <!--light orange: #FFDAB9-->
        
    </v-navigation-drawer>
    


    <main>
    <v-card rounded="0">
      
        <v-divider></v-divider>

         <v-row class="ma-5">
           <v-col>
               <h2>Clustering mittels Künstlicher Intelligenz</h2>
               <v-card-text>Im Folgenden kann analysiert werden, wo sich Ortsteile gemäß gewissen Kategorien zu Gruppen ähnlicher Punkte ballen ("clustern").<p></p>
               Nutzen Sie das eingebautes Machine-Learning-Feature, indem Sie Sie die Ortsteile, die Kategorien und ggf. die Clusteranzahl wählen.<p></p> Letztere können Sie alternativ auch vom Tool optimieren lassen.                                                      
                <p>Bei <strong>zwei Kategorien</strong> können Sie das Ergebnis graphisch betrachten. Dabei können Sie über die Punkte fahren, um genauere Informationen zu erhalten. Generell darf die Clusteranzahl die Ortsteilanzahl nicht übersteigen.</p></v-card-text>
           </v-col>
         </v-row>

         <v-row class="ma-5">
           <v-col>
        
              <div class="bubble-chart-container" id="bubble">
             <BubbleChart
                   ref="bChart"
                   :submitter="this.submitter"
                   :optimieren="this.test"
                   :anzahl="this.anzahl"
                   :orte="this.selectOrte"
                   :kategorie="this.selectKategorie"
                   @kategorie="handleKategorie" 
                   @orte="handleOrte" 
                   @annotliste="handleAnnotliste"
               ></BubbleChart> 
              </div>
      
           </v-col>

         </v-row>

         <v-row>
          <v-col>
            <div id="clusteranzeige" hidden="true">
                      <div v-for="(list, index) in this.outputliste"  :key="index">
                        <p style="font-weight: bold; font-size: 1.2em; margin-left: 10px; margin-right: 10px;">Cluster {{ index +1 }}:</p> 
                        <p style="margin-left: 10px; margin-right: 10px;">{{ list.join(', ') }}</p>
                        <br>
                      </div>
            </div>

          </v-col>
         </v-row>


    </v-card>
    </main>

  </div>
</template>

<script>
import BubbleChart from "@/components/BubbleChart";
export default {
  components: { BubbleChart },
  data(){
    return{
      drawer:true,
      selectOrte: [],
      itemsOrte: [],
      selectKategorie: [],
      itemsKategorie: [],
      anzahl:"2",
      vielDimensional: false,
      annotListe: [],
      selectAll: false,
      optimierer: false,
      test: false,
      outputliste: [["test","test2"],["test4","test5"]],
      submitter: false,
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
        document.getElementById("clusteranzeige").hidden = false
        this.processLists(this.annotListe, this.selectOrte)
        console.log("unser list von lits outputliste")
        console.log(this.outputliste)
      }
      else{
        document.getElementById("bubble").hidden = false
        document.getElementById("clusteranzeige").hidden = true
        this.processLists(this.annotListe, this.selectOrte)
        console.log("unser list von lits outputliste")
        console.log(this.outputliste)
      }
    },
    optimierer(val){
      if (val === true){
        let a = this.selectKategorie
        this.selectKategorie = []
        this.selectKategorie = a
      }
      else{
        let w = this.selectKategorie
        this.selectKategorie = []
        this.selectKategorie = w
      }
    },
    async anzahl(){
      await(this.processLists(this.annotListe, this.selectOrte))
      console.log("unser list von lits outputliste")
      console.log(this.outputliste)
    },
    selectOrte(){
      this.processLists(this.annotListe, this.selectOrte)
      console.log("unser list von lits outputliste")
      console.log(this.outputliste)
    },
    submitter(){
      this.processLists(this.annotListe, this.selectOrte)
      console.log("unser list von lits outputliste")
      console.log(this.outputliste)
    }

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