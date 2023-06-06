<template>
  <q-card class="full-width full-height">
    <q-card-section class="text-h6" v-if="title">{{ title }}</q-card-section>
    <canvas :id="id" class="full-width"></canvas>
  </q-card>
</template>

<script setup>
import * as echarts from "echarts";
import { api } from "src/boot/axios";
const props = defineProps({
  id: String,
  title: String,
  hospital: String,
});
let draw;
import { onMounted, watch } from "vue";
onMounted(() => {
  var chartDom = document.getElementById(props.id);
  const { clientHeight, clientWidth } = chartDom.parentElement;
  chartDom.width = clientWidth;
  chartDom.height = clientHeight;
  console.log(clientHeight);
  var myChart = echarts.init(chartDom);
  var option;
  draw = () => {
    // api.post("/")
    fetch("/line_data.json")
      .then((d) => d.json())
      .then((json) => {
        let tmp = [];
        for (const k in json) {
          tmp.push(json[k]);
        }
        const data = tmp.slice(0, 10);
        option = {
          xAxis: {
            type: "category",
            data: data[0].map((d) => d.time),
          },
          yAxis: {
            type: "value",
          },
          series: data.map((cell) => ({
            data: cell.map((d) => d.count),
            type: "line",
          })),
        };
        console.log(option.series);
        option && myChart.setOption(option);
      });
  };
  draw()
});
watch(props, draw);
</script>
