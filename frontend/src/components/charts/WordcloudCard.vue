<template>
  <q-card class="full-width full-height">
    <q-card-section class="text-h6" v-if="title">{{ title }}</q-card-section>
    <canvas :id="id" class="full-width"></canvas>
  </q-card>
</template>

<script setup>
import * as echarts from "echarts";
import { onMounted } from "vue";
import "echarts-wordcloud";
import * as d3 from "d3";
import { api } from "src/boot/axios";
const props = defineProps({
  id: String,
  title: String,
});

onMounted(() => {
  var chartDom = document.getElementById(props.id);
  const { clientHeight, clientWidth } = chartDom.parentElement;
  chartDom.width = clientWidth;
  chartDom.height = clientHeight;
  var myChart = echarts.init(chartDom);
  let wordCloudColor = d3.schemeDark2;

  myChart.showLoading();
  api.get("/load_wordcloud").then((resp) => {
    const json = resp.data;

    myChart.hideLoading();
    myChart.setOption({
      visualMap: {
        type: "piecewise",
        show: true, // 展示图例
        min: Math.min(...json.map((d) => d.value)),
        max: Math.max(...json.map((d) => d.value)),
        splitNumber: wordCloudColor.length,
        color: wordCloudColor,
      },
      title: {
        text: "疾病频数\n词云图",
        top: "bottom",
        left: "right",
      },
      series: [
        {
          type: "wordCloud",
          gridSize: 14,
          sizeRange: [16, 50],
          rotationRange: [0, 90],
          width: "75%",
          height: "100%",
          //数据
          data: json,
        },
      ],
    });
  });
});
</script>
