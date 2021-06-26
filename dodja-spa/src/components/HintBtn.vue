<template>
  <b-badge
    href="#"
    variant="info"
    class="h5 close m-0 p-0"
    @click="showHint"
    :data="hint_key"
    pill
  >
    <b-icon icon="info-circle" scale="0.8" v-b-toggle.sidebar-left></b-icon>
  </b-badge>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "HintBtn",
  props: ["hint_key"],
  computed: {
    ...mapGetters(["language"]),
    div_id: function () {
      return String(this.hint_key) + "_hint";
    }
  },
  methods: {
    ...mapActions(["loadHint"]),
    showHint: async function () {
      await this.loadHint(this.hint_key);
    }
  }
};
</script>
