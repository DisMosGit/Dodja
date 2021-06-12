<template>
  <div>
    <h1>
      {{ $t("profile") | capitalize }} <code>{{ user.username }}</code>
    </h1>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
export default {
  name: "Profile",
  computed: {
    ...mapGetters(["auth", "user", "message"])
  },
  methods: {
    ...mapMutations(["setMsg"])
  }
};
</script>
