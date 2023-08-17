<template>
    <Bubble class="bubblechart"
          :options="chartOptions"
          :id="chartId"
          :dataset-id-key="datasetIdKey"
          :plugins="plugins"
          :css-classes="cssClasses"
          :styles="styles"
          :width="width"
          :height="height"
          :data="chartData"
    />
  </template>
  
  <script>
  import { Bubble } from 'vue-chartjs'
  import {
    Chart as ChartJS,  Title,  Tooltip,  Legend,  LineElement,  LinearScale,  PointElement,  CategoryScale,} from 'chart.js'
  ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale)
  
  export default {
    name: 'BubbleChart',
    components: {Bubble},
    props: {
      chartId: {
        type: String,
        default: 'bubble-chart'
      },
      anzahl: {
        type: String,
        default: "2",
      },
      orte:{ 
        type: Array,
      },
      kategorie:{
        type: Array,
      },
      submitter:{
        type: Boolean,
      },
      datasetIdKey: {
        type: String,
        default: 'label'
      },
      width: {
        type: Number,
        default: 500
      },
      height: {
        type: Number,
        default: 500,
      },
      cssClasses: {
        default: '',
        type: String
      },
      styles: {
        type: Object,
        default: () => {}
      },
      plugins: {
        type: Object,
        default: () => {}
      },
      optimieren:{
        type: Boolean,
      }
    },
    methods:{
      //aktualisiert das Diagramm
      updateDiagramm(newData){

        let b;
        let x;

        let Altenquote = []
        let DurchschnittlicheHaushaltsgröße = []
        let Durchschnittsalter = []
        let Elektroautos = []
        let Jugendquote = []
        let KinderInTagesbetreuung = []
        let LebenszufriedenheitZufriedenheitsfaktor = []
        let PersönlichesEinkommen = []
        let Straftaten = []
        let WirtschaftlicheLageZufriedenheitsfaktor = []
        let WohnviertelZufriedenheitsfaktor = []
        let ZukunftsaussichtZufriedenheitsfaktor = []

        let annot = [] //labels?
        let ortsteil = []

        let kategorielist =["Altenquote","DurchschnittlicheHaushaltsgröße","Durchschnittsalter","Elektroautos",
                "Jugendquote","KinderInTagesbetreuung", "LebenszufriedenheitZufriedenheitsfaktor","PersönlichesEinkommen",
                "Straftaten","WirtschaftlicheLageZufriedenheitsfaktor", "WohnviertelZufriedenheitsfaktor",
                "ZukunftsaussichtZufriedenheitsfaktor"]
        
        let ortsteillist =['Althen-Kleinpösna', 'Altlindenau', 'Anger-Crottendorf', 'Baalsdorf',
                            'Burghausen-Rückmarsdorf', 'Böhlitz-Ehrenberg', 'Connewitz', 'Dölitz-Dösen',
                            'Engelsdorf', 'Eutritzsch', 'Gohlis-Mitte', 'Gohlis-Nord', 'Gohlis-Süd',
                            'Großzschocher', 'Grünau-Mitte', 'Grünau-Nord', 'Grünau-Ost',
                            'Grünau-Siedlung', 'Hartmannsdorf-Knautnaundorf', 'Heiterblick',
                            'Holzhausen', 'Kleinzschocher', 'Knautkleeberg-Knauthain', 'Lausen-Grünau',
                            'Leutzsch', 'Liebertwolkwitz', 'Lindenau', 'Lindenthal', 'Lößnig',
                            'Lützschena-Stahmeln', 'Marienbrunn', 'Meusdorf', 'Miltitz', 'Mockau-Nord',
                            'Mockau-Süd', 'Möckern', 'Mölkau', 'Neulindenau', 'Neustadt-Neuschönefeld',
                            'Paunsdorf', 'Plagwitz', 'Plaußig-Portitz', 'Probstheida',
                            'Reudnitz-Thonberg', 'Schleußig', 'Schönau', 'Schönefeld-Abtnaundorf',
                            'Schönefeld-Ost', 'Seehausen', 'Sellerhausen-Stünz', 'Stötteritz',
                            'Südvorstadt', 'Thekla', 'Volkmarsdorf', 'Wahren', 'Wiederitzsch', 'Zentrum',
                            'Zentrum-Nord', 'Zentrum-Nordwest', 'Zentrum-Ost', 'Zentrum-Süd',
                            'Zentrum-Südost', 'Zentrum-West']

        //put API-Data into variables 
        for(b in newData){
          Altenquote.push(newData[b].Altenquote)
          DurchschnittlicheHaushaltsgröße.push(newData[b].DurchschnittlicheHaushaltsgröße)
          Durchschnittsalter.push(newData[b].Durchschnittsalter)
          Elektroautos.push(newData[b].Elektroautos)
          Jugendquote.push(newData[b].Jugendquote)
          KinderInTagesbetreuung.push(newData[b].KinderInTagesbetreuung)
          LebenszufriedenheitZufriedenheitsfaktor.push(newData[b].LebenszufriedenheitZufriedenheitsfaktor)
          PersönlichesEinkommen.push(newData[b].PersönlichesEinkommen)
          Straftaten.push(newData[b].Straftaten)
          WirtschaftlicheLageZufriedenheitsfaktor.push(newData[b].WirtschaftlicheLageZufriedenheitsfaktor)
          WohnviertelZufriedenheitsfaktor.push(newData[b].WohnviertelZufriedenheitsfaktor)
          ZukunftsaussichtZufriedenheitsfaktor.push(newData[b].ZukunftsaussichtZufriedenheitsfaktor)
      
          annot.push(newData[b].label) //anotation
          ortsteil.push(newData[b].Ortsteil)
        }

        //at first data for bubble chart is empty
        this.chartData = {
          datasets:[]
        }
        
        //fill data as desired
        //only if two categories are selected in combobox
        if ((this.kategorie).length === 2){
          let firstCateg = this.kategorie[0]
          let secondCateg = this.kategorie[1]
 
          for (x in ortsteil){
            this.chartData.datasets.push(
              {  
                label: ortsteil[x], //point's identifier in the diagramm
                backgroundColor: this.colors[annot[x]], //real label/anotation
                data:[
                  { 
                    x:(eval(firstCateg))[x],
                    y:(eval(secondCateg))[x], 
                    r:10, // point's radius
                  }
                ]
              }
              )
          }
        }

       // mit eigenen Werten testen
       this.$emit("orte", ortsteillist)
       this.$emit("kategorie", kategorielist) //first argument: event name ; second argument: payload
       this.$emit("annotliste", annot)

      },
      
      //lädt die Daten von der API
      async loadData(){
        this.loaded = false
        try {

          //spezifischer API-call hin für die ausgewählten Ortsteile und Kategorien
          const desired_ortsteile = this.orte
          const desired_kategorien = this.kategorie

          const kategorielist_standard =["Altenquote","DurchschnittlicheHaushaltsgröße","Durchschnittsalter","Elektroautos",
                "Jugendquote","KinderInTagesbetreuung", "LebenszufriedenheitZufriedenheitsfaktor","PersönlichesEinkommen",
                "Straftaten","WirtschaftlicheLageZufriedenheitsfaktor", "WohnviertelZufriedenheitsfaktor",
                "ZukunftsaussichtZufriedenheitsfaktor"]
        
          const ortsteillist_standard =['Althen-Kleinpösna', 'Altlindenau', 'Anger-Crottendorf', 'Baalsdorf',
                            'Burghausen-Rückmarsdorf', 'Böhlitz-Ehrenberg', 'Connewitz', 'Dölitz-Dösen',
                            'Engelsdorf', 'Eutritzsch', 'Gohlis-Mitte', 'Gohlis-Nord', 'Gohlis-Süd',
                            'Großzschocher', 'Grünau-Mitte', 'Grünau-Nord', 'Grünau-Ost',
                            'Grünau-Siedlung', 'Hartmannsdorf-Knautnaundorf', 'Heiterblick',
                            'Holzhausen', 'Kleinzschocher', 'Knautkleeberg-Knauthain', 'Lausen-Grünau',
                            'Leutzsch', 'Liebertwolkwitz', 'Lindenau', 'Lindenthal', 'Lößnig',
                            'Lützschena-Stahmeln', 'Marienbrunn', 'Meusdorf', 'Miltitz', 'Mockau-Nord',
                            'Mockau-Süd', 'Möckern', 'Mölkau', 'Neulindenau', 'Neustadt-Neuschönefeld',
                            'Paunsdorf', 'Plagwitz', 'Plaußig-Portitz', 'Probstheida',
                            'Reudnitz-Thonberg', 'Schleußig', 'Schönau', 'Schönefeld-Abtnaundorf',
                            'Schönefeld-Ost', 'Seehausen', 'Sellerhausen-Stünz', 'Stötteritz',
                            'Südvorstadt', 'Thekla', 'Volkmarsdorf', 'Wahren', 'Wiederitzsch', 'Zentrum',
                            'Zentrum-Nord', 'Zentrum-Nordwest', 'Zentrum-Ost', 'Zentrum-Süd',
                            'Zentrum-Südost', 'Zentrum-West']
          
          const ortsteileBinaryList = ortsteillist_standard.map(u => desired_ortsteile.includes(u) ? 1 : 0);
          const kategorienBinaryList = kategorielist_standard.map(p => desired_kategorien.includes(p) ? 1 : 0);

          const clusteranzahl = this.anzahl

          /* Testing
          let ortsteileBinaryList = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1
                                    , 1, 1, 1, 0, 1, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 
                                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
          let kategorienBinaryList = [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
          */

          let ortsteileBinaryString = ortsteileBinaryList.join('');
          let kategorienBinaryString = kategorienBinaryList.join('');

          /* Optimierung -> ohne Übergabe Clusteranzahl (k) ; Nicht-Optimierung -> mit Übergabe Clusteranzahl (k) */
          if (this.optimieren === true){
            this.bubbleChartData = await (await fetch(
              "http://127.0.0.1:5000/get/kmeansWithoutk?"
                +"ortsteile_string="+ortsteileBinaryString
                +"&kategorien_string="+kategorienBinaryString)).json()
                ;
              }
          else{
            this.bubbleChartData = await (await fetch(
              "http://127.0.0.1:5000/get/kmeansWithk?clusteranzahl="+clusteranzahl
                +"&ortsteile_string="+ortsteileBinaryString
                +"&kategorien_string="+kategorienBinaryString)).json()
                ;
                //Test: http://127.0.0.1:5000/get/kmeansWithk?clusteranzahl=3&ortsteile_string=111111111111101000000000000101111111111100000000000000000011111&kategorien_string=111111111111
          }
          this.updateDiagramm(this.bubbleChartData)
          this.loaded = true
        }catch (e){
          console.error(e)
        }
      },
      refresh(val){
          if (val=="true"){
            this.loadData()
          }
      }
    },
    watch:{ //läuft die ganze Zeit
      //checks change in anzahl and calls if any loadData()
      anzahl:function(){
        this.loadData()
      },
      orte:function(){
        this.loadData()
      },
      kategorie:function(){
        this.loadData()
      },
      optimieren:function(){
        this.loadData()
      },
      submitter:function(){
        this.loadData()
      },
    },
  
    data(){
      return{
        loaded:false,
        colors: ['#4527A0', '#F44336', '#66BB6A', '#FFF176', '#9C27B0', '#FFB74D', '#AED581', '#DCE775', '#FFD54F', '#4527A0', '#283593', '#D32F2F', '#C2185B', '#7B1FA2', '#512DA8', '#303F9F', '#B71C1C', '#E53935', '#D81B60', '#8E24AA', '#5E35B1', '#3949AB', '#EF5350', '#EC407A', '#AB47BC', '#7E57C2', '#5C6BC0', '#E57373', '#F06292', '#BA68C8', '#9575CD', '#7986CB', '#EF9A9A', '#F48FB1', '#CE93D8', '#B39DDB', '#9FA8DA', '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50', '#0D47A1', '#01579B', '#006064', '#004D40', '#1B5E20', '#1565C0', '#0277BD', '#00838F', '#00695C', '#2E7D32', '#1976D2', '#0288D1', '#0097A7', '#00796B', '#388E3C', '#1E88E5', '#039BE5', '#00ACC1', '#00897B', '#43A047', '#42A5F5', '#29B6F6', '#26C6DA', '#26A69A', '#66BB6A', '#64B5F6', '#4FC3F7', '#4DD0E1', '#4DB6AC', '#81C784', '#90CAF9', '#81D4FA', '#80DEEA', '#80CBC4', '#A5D6A7', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107', '#FF9800', '#33691E', '#827717', '#F57F17', '#FF6F00', '#E65100', '#558B2F', '#9E9D24', '#F9A825', '#FF8F00', '#EF6C00', '#689F38', '#AFB42B', '#FBC02D', '#FFA000', '#F57C00', '#7CB342', '#C0CA33', '#FDD835', '#FFB300', '#673AB7', '#3F51B5', '#FB8C00', '#9CCC65', '#D4E157', '#FFEE58', '#FFCA28', '#FFA726'],
        chartData:{
          datasets:[]
        },
        chartOptions:{
          responsive:true,
          maintainAspectRatio: true,
          plugins:{
            legend: {
              display: false,
            },
            title:{
              display: false,
            },
          },
          scales: {
            x: {
              display: true,
              title: {
                display: true,
                text:'Erst ausgewählte Kategorie'
              },
              //suggestedMin: 0,
            },
            y: {
              display: true,
              title: {
                display: true,
                text:'Zweit ausgewählte Kategorie'
              },
              //suggestedMin: 0,
            }
          }
        }
      }
    },
    //bevor das Diagramm lädt
    async mounted(){
      await this.loadData()
    }
  }
  </script>
  
  <style scoped>
  </style>