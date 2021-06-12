<template>
  <b-sidebar id="sidebar-left" sidebar-class="border" shadow lazy>
    <template #header="{ hide }">
      <b-button block variant="outline-danger" size="sm" @click="hide">
        {{ $t("close") | capitalize }}
      </b-button>
    </template>
    <div id="sidebar-left-content" class="p-2">
      <Hint
        v-for="hint in loadedHints.slice().reverse()"
        v-bind:key="hint.key"
        v-bind:hint="hint"
      ></Hint>
    </div>
  </b-sidebar>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import Hint from "@/components/Hint";

export default {
  name: "SidebarLeft",
  components: {
    Hint
  },
  computed: {
    ...mapGetters(["loadedHints"])
  },
  methods: {
    ...mapActions(["deleteAllHints"])
  }
};
</script>
