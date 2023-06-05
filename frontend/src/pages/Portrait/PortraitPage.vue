<template>
  <q-tabs
    v-model="tab"
    dense
    class="text-grey"
    active-color="primary"
    indicator-color="primary"
    align="left"
    narrow-indicator
  >
    <q-tab name="user" label="客户" />
    <q-tab name="hospital" label="医院" />
  </q-tabs>

  <q-separator />

  <q-tab-panels v-model="tab" animated>
    <q-tab-panel name="user">
      <portrait-user></portrait-user>
    </q-tab-panel>

    <q-tab-panel name="hospital">
      <portrait-hospital></portrait-hospital>
    </q-tab-panel>
  </q-tab-panels>
</template>

<script setup>
import { ref } from "vue";
import PortraitHospital from "./HospitalPage.vue";
import PortraitUser from "./UserPage.vue";

const tab = ref("user");
</script>
