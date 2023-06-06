<template>
  <q-card class="full-width full-height">
    <q-card-section class="text-h6" v-if="title">{{ title }}</q-card-section>
    <canvas :id="id" class="full-width"></canvas>
  </q-card>
</template>

<script setup>
import * as echarts from "echarts";
const props = defineProps({
  id: String,
  title: String,
});

import { onMounted } from "vue";
onMounted(() => {
  var chartDom = document.getElementById(props.id);
  const { clientHeight, clientWidth } = chartDom.parentElement;
  chartDom.width = clientWidth;
  chartDom.height = clientHeight;
  console.log(clientHeight);
  var myChart = echarts.init(chartDom);
  var option;

  option = {
    xAxis: {
      type: "category",
      data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: [120, 200, 150, 80, 70, 110, 130],
        type: "bar",
      },
    ],
  };
  option && myChart.setOption(option);
});
</script>
