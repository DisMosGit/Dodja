<template>
  <b-dropdown
    split
    v-on:click="goDocker(manager.route)"
    :text="manager.name"
    dropup
    variant="outline-info"
    menu-class="w-100"
  >
    <b-dropdown-item
      v-for="category in categories"
      v-bind:key="category.name"
      v-on:click="goDocker(category.route)"
      >{{ category.name }}</b-dropdown-item
    >
  </b-dropdown>
</template>

<script>
export default {
  name: "DockerBtn",
  props: ["host_id"],
  data() {
    return {
      categories: [
        { name: "Container", route: "HostContainerList" },
        { name: "Image", route: "HostImageList" },
        { name: "Volume", route: "HostVolumeList" },
        { name: "Network", route: "HostNetworkList" }
      ],
      manager: { name: "Docker", route: "HostDocker" }
    };
  },
  methods: {
    goDocker(route) {
      this.$router.push({
        name: route,
        params: { id: this.host_id }
      });
    }
  }
};
</script>
