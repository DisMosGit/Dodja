<template>
  <b-jumbotron border-variant="dark" class="col-md-auto m-2 p-3">
    <h2 class="text-center">
      <b-badge variant="light">{{ host.id | cut(0, 8) }}</b-badge>
      {{ host.title }}
      <HintBtn v-bind:hint_key="'test'"></HintBtn>
    </h2>
    <p>{{ host.description | cut(0, 40) }}</p>
    <hr class="my-2" />
    <p>
      {{ host.credentials.base_url }}
    </p>
    <b-button-group>
      <b-button variant="primary" v-on:click="goDetail()">
        {{ $tc("detail", 1) | capitalize }}
      </b-button>
      <DockerBtn v-bind:host_id="host.id" />
    </b-button-group>
  </b-jumbotron>
</template>

<script>
export default {
  name: "Host",
  components: {
    DockerBtn: () => import("./DockerBtn.vue")
  },
  props: ["host", "docker"],
  methods: {
    goDetail: function() {
      this.$router.push({
        name: "HostDetail",
        params: { id: this.host.id }
      });
    },
    goDocker: function() {
      this.$router.push({
        name: "HostDocker",
        params: { id: this.host.id }
      });
    }
  }
};
</script>
