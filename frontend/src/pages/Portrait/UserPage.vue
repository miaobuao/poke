<template>
  <div class="row">
    <div class="col-12 col-md-6 q-pa-md">
      <network-card id="phauodife"></network-card>
    </div>
    <div class="col-12 col-md-6 q-pa-md"><wordcloud-card id="1212"></wordcloud-card></div>
    <div class="col-12 col-md-12 q-pa-md">
      <river-card id="121212"></river-card>
    </div>
  </div>
</template>

<script setup>
import PieCard from "src/components/charts/PieCard.vue";
import NetworkCard from "src/components/charts/NetworkCard.vue";
import WordcloudCard from "src/components/charts/WordcloudCard.vue";
import RiverCard from "src/components/charts/RiverCard.vue";
</script>
