<template>
  <div class="container">
          <v-row class="ma-5">
           <v-col>
               <h2>Herzlich Willkommen!</h2>
               <div class="spacer"></div>
               <h3>Über die Reiter auf der linken Seite gelangen Sie zur gewünschten Thematik zur Datenbankkommunikation!</h3>
           </v-col>
         </v-row>

  <main>
    <div class="image-container">
      <img
        :src="require('@/assets/databasepic.jpg')"
        alt=" "
        class="image"
      >
    </div>
    <div class="caption"></div>

    <br>
    <br>

    
    <v-btn @click="handleClick" class="custom-pink-button">Anwendung beenden (Finish)</v-btn>

  </main>
  
</div>

</template>

<script>
export default {
  methods: {
    handleClick() {
      // Aktion bei klick
      alert('Anwendung wurde beendet. Bitte den Browser schließen.');
    }
  }
};
</script>



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
/* Stil für den benutzerdefinierten rosa Button */
.custom-pink-button {
  background-color: #fce4ec; /* Rosa Hintergrundfarbe */
  color: #333; /* Textfarbe */
  margin-left: 10px;
}

.custom-pink-button:hover {
  background-color: #ffC0cb; /* Farbänderung im Hover-Zustand */
}



</style>


