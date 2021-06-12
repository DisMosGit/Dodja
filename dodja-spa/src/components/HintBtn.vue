<template>
  <div class="close" @click="showHint" :data="hint_key">
    <b-icon
      icon="info-circle"
      scale="0.8"
      variant="info"
      v-b-toggle.sidebar-left
    ></b-icon>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "HintBtn",
  props: ["hint_key"],
  computed: {
    ...mapGetters(["language"]),
    div_id: function() {
      return String(this.hint_key) + "_hint";
    }
  },
  methods: {
    ...mapActions(["loadHint"]),
    showHint: async function() {
      await this.loadHint(this.hint_key);
    }
  }
};
</script>
