<template>
  <div>
    <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
      <q-file
        outlined
        v-model="file"
        :rules="[
          (val) => !!val || 'Please select file',
          (val) =>
            ['csv', 'xlsx', 'xls'].findIndex(
              (v) => getSuffix(val.name) === v
            ) != -1 || 'not in [csv, xlxs, xls]',
        ]"
      >
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
      </q-file>

      <div>
        <q-btn label="Submit" type="submit" color="primary" />
        <q-btn
          label="Reset"
          type="reset"
          color="primary"
          flat
          class="q-ml-sm"
        />
      </div>
    </q-form>
    <template v-if="predict.length">
      <q-select
        class="q-pt-md"
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
      <rank-card
        class="q-pt-md"
        v-if="selected.length"
        id="rank-chart"
        :data="selected"
      ></rank-card>
    </template>
  </div>
</template>

<script setup>
import { useQuasar } from "quasar";
import RankCard from "src/components/charts/RankCard.vue";
import { api } from "src/boot/axios";
import { ref } from "vue";
const $q = useQuasar();
const age = ref();
const name = ref("");
const predict = ref([]);
const file = ref();
const selected = ref([]);
const filterOptions = ref([]);
function getSuffix(name) {
  return name.split(".").reverse()[0];
}
function onSubmit() {
  let formData = new FormData();
  formData.append("file", file.value);
  api.post("/upload", formData).then((resp) => {
    const { data } = resp;
    if (data.message)
      predict.value = data.message.map((d, idx) => {
        d.id = idx;
        return d;
      });
    else if (data.error)
      $q.notify({
        type: "negative",
        message: data.error,
      });
  });
}

function onReset() {
  file.value = undefined;
}

let filter_val = "";
function updateFilterOptions(value) {
  filterOptions.value = (
    predict.value?.filter(
      (d) => value.findIndex((v) => d.id === v.id) === -1
    ) ?? []
  ).filter((v) => v[0].toLowerCase().indexOf(filter_val) > -1);
}

function filterFn(val, update) {
  filter_val = val.trim().toLowerCase();
  if (filter_val) {
    const opt = predict.value;
    update(() => {
      filterOptions.value = opt
        .filter((v) => v[0].toLowerCase().indexOf(filter_val) > -1)
        .filter((v) => selected.value.findIndex((d) => d.id === v.id) == -1);
    });
  } else
    update(() => {
      filterOptions.value = predict.value.filter(
        (v) => selected.value.findIndex((d) => d.id === v.id) == -1
      );
    });
}
</script>
