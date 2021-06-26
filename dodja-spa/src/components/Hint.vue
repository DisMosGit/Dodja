<template>
  <b-card :title="hint.title" class="text-center">
    <b-card-sub-title class="mb-2">{{
      hint.date_updated | toDate
    }}</b-card-sub-title>
    <b-card-text class="text-justify text-wrap text-break">
      {{ hint.text }}
    </b-card-text>
    <b-button-group size="sm">
      <b-button variant="danger" v-on:click="deleteMe()">Delete</b-button>
      <b-button variant="warning" v-on:click="deleteMe()">Refresh</b-button>
    </b-button-group>
  </b-card>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "Hint",
  props: ["hint"],
  methods: {
    ...mapMutations(["deleteHintByKey"]),
    deleteMe: function () {
      this.deleteHintByKey(this.hint.key);
    }
  }
};
</script>
