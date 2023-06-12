<template>
  <div>
  <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
    <q-file
      outlined
      v-model="file"
      :rules="[
        (val) => !!val || 'Please select file',
        (val) =>
          ['csv', 'xlsx', 'xls'].findIndex((v) => getSuffix(val.name) === v) !=
            -1 || 'not in [csv, xlxs, xls]',
      ]"
    >
      <template v-slot:prepend>
        <q-icon name="attach_file" />
      </template>
    </q-file>

    <div>
      <q-btn label="Submit" type="submit" color="primary" />
      <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
    </div>
  </q-form>
  <rank-card id="rank-chart" v-if="predict.length" :data="predict"></rank-card>
  </div>
</template>

<script setup>
import RankCard from "src/components/charts/RankCard.vue";
import { api } from "src/boot/axios";
import { ref } from "vue";
const age = ref();
const name = ref("");
const predict = ref([])
const file = ref();
function getSuffix(name) {
  return name.split(".").reverse()[0];
}
function onSubmit() {
  let formData = new FormData();
  formData.append("file", file.value);
  api
    .post("/upload", formData)
    .then((d) => console.log(d))
    .catch((resp) => {
      console.log(resp);
      predict.value = resp.data
    });
}

function onReset() {}
// api.post
</script>
