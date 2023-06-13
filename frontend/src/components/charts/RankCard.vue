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
  data: Array,
});

import { onMounted, watch } from "vue";
function draw() {
  let chartDom = document.getElementById(props.id);
  const { clientHeight, clientWidth } = chartDom.parentElement;
  chartDom.width = clientWidth;
  chartDom.height = clientHeight;
  console.log(clientHeight);
  let myChart = echarts.init(chartDom);
  let option;

  option = {
    title: {
      text: "欺诈风险概率rk图",
      top: "top",
      left: "center",
    },
    xAxis: {
      max: "dataMax",
    },
    yAxis: {
      type: "category",
      data: props.data.map((d) => d[0]),
      inverse: true,
      animationDuration: 300,
      animationDurationUpdate: 300,
    },
    series: [
      {
        realtimeSort: true,
        data: props.data.map((d) => d[1]),
        type: "bar",
      },
    ],
  };
  option && myChart.setOption(option);
}
onMounted(() => {
  draw();
});
watch(props, draw);
</script>
