<template>
  <q-card class="full-width full-height">
    <q-card-section class="text-h6">{{ title }}</q-card-section>
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
  var option;

  myChart.showLoading();
  fetch("/network_data.json")
    .then((d) => d.json())
    .then((json) => {
      myChart.hideLoading();
      myChart.setOption(
        (option = {
          title: {
            text: "欺诈风险网络图",
            top: "bottom",
            left: "right",
          },
          tooltip: {},
          legend: [
            {
              // selectedMode: 'single',
              data: json.categories.map(function (a) {
                return a.name;
              }),
            },
          ],
          animationDurationUpdate: 1500,
          animationEasingUpdate: "quinticInOut",
          series: [
            {
              name: "Les Miserables",
              type: "graph",
              layout: "force",
              force: {
                initLayout: "circular",
                gravity: 0,
                repulsion: 800,
                edgeLength: 2,
              },
              data: json.nodes,
              links: json.links,
              categories: json.categories,
              roam: true,
              label: {
                position: "right",
                formatter: "{b}",
              },
              lineStyle: {
                color: "source",
                curveness: 0.3,
              },
              emphasis: {
                focus: "adjacency",
                lineStyle: {
                  width: 10,
                },
              },
            },
          ],
        })
      );
    });
});
</script>
