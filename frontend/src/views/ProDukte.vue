<template>
    <div>
    <!-- Navigations-Bar rechts zum einstellen der Diagramme -->
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
        ></v-combobox>

      </v-navigation-drawer>



    <main>
      <v-card rounded="0">

        <v-row class="ma-5">
           <v-col>
               <h2>Wertevergleich</h2>
               <v-card-text>Im Folgenden können gewählte Ortsteile hinsichtlich bestimmter Kategorien in einem Balkendiagramm graphisch veranschaulicht werden.
                Fahren Sie zudem über einen Balken, um genauere Informationen zu erhalten. Dieses einführende Feature soll Ihnen helfen,
                sich einen Überblick über die Daten zu verschaffen und deskriptive Vergleiche ziehen zu können. 
                </v-card-text>
           </v-col>
         </v-row>

         <v-row class="mx-15 my-3"> <!-- Added margin utility classes mx-5 and my-3 for horizontal and vertical spacing -->
          <v-col>
            <div class="bar-chart-container" id="bar">
            <BarChart
                  ref="barChart"
                  :orte="this.selectOrte"
                  :kategorie="this.selectKategorie"
                  @kategorie="handleKategorie" 
                  @orte="handleOrte" 
            ></BarChart>
          </div>
          </v-col>
         </v-row>
     
      </v-card>
    </main>
    
    </div>

</template>

<script>
    import BarChart from "@/components/BarChart"
    
    export default{
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
  .bar-chart-container { /*so passt es auf normal großen Bildschirm */
    max-width: 2000px; 
    max-height: 650px; 
    margin: 0 auto; /* Center the chart horizontally */ 
  }
  </style>


