<template>
  <div class="container">
          <v-row class="ma-5">
           <v-col>
               <h2>Willkommen zu MIRA!</h2>
               <div class="spacer"></div>
               <h3>Lassen Sie sich von der Macht des maschinellen Lernens begeistern und nutzen Sie dieses KI-Analysetool, um Leipzig aus einem neuen Blickwinkel zu entdecken. 
                Vergleichen Sie die 63 Ortsteile der Stadt hinsichtlich 12 Kategorien mit realen Daten für das Jahr 2021 und erkennen Sie spannende Zusammenhänge auf einfache Art!</h3>
           </v-col>
         </v-row>

  <main>
    <div class="image-container">
      <img
        :src="require('@/assets/NeuesRathausDrei.jpg')"
        alt="Foto der Stadt Leipzig"
        class="image"
      >
    </div>
    <div class="caption">Foto: © Stadt Leipzig</div>

  </main>
  
</div>

</template>

<style>
.spacer {
    margin-bottom: 30px; /* Adjust the value to increase or decrease the space */
}
.container {
  position: relative;
}
.image-container {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* Adjust the margin as desired */
}
.image {
  max-width: 100%;
  max-height: 70%;
}
.caption {
  text-align: right;
  margin-top: 4px;
  font-style: italic;
  margin-right: 20px;
}


</style>
