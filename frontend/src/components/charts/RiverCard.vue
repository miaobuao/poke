<template>
  <q-card class="full-width full-height">
    <q-card-section class="text-h6" v-if="title">{{ title }}</q-card-section>
    <canvas :id="id" class="full-width"></canvas>
  </q-card>
</template>

<script setup>
import * as echarts from "echarts";
import { onMounted } from "vue";

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

  myChart.showLoading();
  fetch("/flow_data.json")
    .then((d) => d.json())
    .then((json) => {
      const legend = {};
      json.forEach((e) => (legend[e.group] = (legend[e.group] ?? 0) + 1));
      myChart.hideLoading();
      const opt = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "line",
            lineStyle: {
              color: "rgba(0,0,0,0.2)",
              width: 1,
              type: "solid",
            },
          },
        },
        legend: {
          data: legend,
        },
        singleAxis: {
          top: 50,
          bottom: 50,
          axisTick: {},
          axisLabel: {},
          type: "time",
          axisPointer: {
            animation: true,
            label: {
              show: true,
            },
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: "dashed",
              opacity: 0.2,
            },
          },
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
        series: [
          {
            type: "themeRiver",
            emphasis: {
              itemStyle: {
                shadowBlur: 20,
                shadowColor: "rgba(0, 0, 0, 0.8)",
              },
            },
            data: json.map(e=>{
              return [
                e.time, e.value, e.group
              ]
            }),
          },
        ],
      }
      console.log(opt.series[0].data);
    });
});
</script>
