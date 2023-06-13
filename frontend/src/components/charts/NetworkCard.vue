<template>
  <q-card class="full-width full-height">
    <q-card-section class="text-h6">{{ title }}</q-card-section>
    <canvas :id="id" class="full-width"></canvas>
  </q-card>
</template>

<script setup>
import * as echarts from "echarts";
import { onMounted } from "vue";
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
  var option;

  myChart.showLoading();
  api.get("/load_network").then((resp) => {
    const json = resp.data;
    myChart.hideLoading();
    myChart.setOption(
      (option = {
        title: {
          text: "智能风控网络图",
          top: "bottom",
          left: "right",
        },
        tooltip: {
          // z: 60,
          // show: true,
          // showContent: true,
          // trigger: "item",
          // triggerOn: "mousemove | click",
          // alwaysShowContent: false,
          // displayMode: "single",
          // renderMode: "auto",
          // confine: null,
          // showDelay: 0,
          // hideDelay: 100,
          // transitionDuration: 0.4,
          // enterable: false,
          // backgroundColor: "#fff",
          // shadowBlur: 10,
          // shadowColor: "rgba(0, 0, 0, 0.2)",
          // shadowOffsetX: 1,
          // shadowOffsetY: 2,
          // borderRadius: 4,
          // borderWidth: 1,
          // padding: null,
          // extraCssText: "",
          // axisPointer: {
          //   type: "line",
          //   axis: "auto",
          //   animation: "auto",
          //   animationDurationUpdate: 200,
          //   animationEasingUpdate: "exponentialOut",
          //   crossStyle: {
          //     color: "#999",
          //     width: 1,
          //     type: "dashed",
          //   },
          // },
          // textStyle: {
          //   color: "#666",
          //   fontSize: 14,
          // },
        },
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
              formatter: function (params) {
                // 设置提示框内容的格式化函数
                if (params.dataType == "edge") {
                  console.log(params.data.source + " > " + params.data.target);
                  // 如果是边缘，则显示源节点和目标节点
                  return params.data.source + " > " + params.data.target;
                } else {
                  // 如果是节点，则显示节点名称和数值
                  return params.data.name + ": " + params.data.value;
                }
              },
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
