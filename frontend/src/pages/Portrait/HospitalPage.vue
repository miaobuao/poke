<template>
  <div class="row full-height q-pa-md q-gutter-md full-width">
    <div class="col-3 full-width">
      <q-card class="full-width q-pa-md">
        <q-select
          filled
          v-model="selected"
          use-input
          use-chips
          multiple
          input-debounce="0"
          :options="filterOptions"
          @update:model-value="updateFilterOptions"
          @filter="filterFn"
        >
        </q-select>
      </q-card>
    </div>
    <div class="col-9 full-width">
      <line-card
        title="医疗机构的欺诈频次折线图"
        id="hospital-line-card"
        class="full-width"
        :hospitals="selected"
      ></line-card>
    </div>
    <!-- </div> -->
  </div>
</template>

<script setup>
import { ref } from "vue";
import LineCard from "src/components/charts/LineCard.vue";
import { api } from "src/boot/axios";
const hospitals = ref([]);
const selected = ref([]);
const filterOptions = ref([]);
let filter_val = "";

function updateFilterOptions(value) {
  filterOptions.value = (
    hospitals.value?.filter((d) => value.findIndex((v) => d === v) === -1) ?? []
  ).filter((v) => v.toLowerCase().indexOf(filter_val) > -1);
}

function filterFn(val, update) {
  filter_val = val.trim().toLowerCase();
  if (filter_val) {
    const opt = hospitals.value;
    update(() => {
      filterOptions.value = opt
        .filter((v) => v.toLowerCase().indexOf(filter_val) > -1)
        .filter((v) => selected.value.indexOf(v) == -1);
    });
  } else
    api.get("/load_hospital").then((resp) => {
      const opt = resp.data;
      hospitals.value = opt;
      update(() => {
        filterOptions.value = opt.filter(
          (v) => selected.value.indexOf(v) == -1
        );
      });
    });
}
</script>
