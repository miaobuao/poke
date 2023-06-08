<template>
  <!-- <div class="full-width full-height absolute"> -->
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

  <q-tab-panels v-model="tab" animated  class="full-width full-height">
    <q-tab-panel name="user" class="full-width full-height">
      <portrait-user class="full-width full-height"></portrait-user>
    </q-tab-panel>

    <q-tab-panel name="hospital" class="full-width full-height">
      <portrait-hospital class="full-width full-height"></portrait-hospital>
    </q-tab-panel>
  </q-tab-panels>
  <!-- </div> -->
</template>

<script setup>
import { ref } from "vue";
import PortraitHospital from "./HospitalPage.vue";
import PortraitUser from "./UserPage.vue";

const tab = ref("user");
</script>
