<template>
  <b-jumbotron border-variant="dark" class="col-md-auto m-1 p-1 shadow-sm">
    <h2 class="text-break">
      <b-badge :variant="this.colors[container.State]">
        {{ container.Id | cut(0, 10) }} </b-badge
      ><HintBtn hint_key="ru_host_container"></HintBtn>
      <p
        class="text-break m-0"
        v-for="name in container.Names"
        v-bind:key="name"
      >
        {{ name | cut(1) }}
      </p>
      <b-badge variant="light">{{ container.Created | toDate("ms") }}</b-badge>
    </h2>
    <p class="text-break">{{ container.State }}: {{ container.Status }}</p>
    <p class="text-break">
      {{ container.Image | cut(0, 32) }}: {{ container.ImageID | cut(0, 20) }}
    </p>
    <hr class="my-2" />
    <p
      class="text-break m-0"
      v-for="(port, key) in container.Ports"
      v-bind:key="key"
    >
      {{ port.PrivatePort }}->{{ port.IP }}:{{ port.PublicPort }}
    </p>
    <p
      class="text-break m-0"
      v-for="(mount, key) in container.Mounts"
      v-bind:key="key"
    >
      {{ mount.Source }}->{{ mount.Destination }}
    </p>
    <hr class="my-2" />
    <b-button-group>
      <b-button variant="primary" v-on:click="goDetail()"> Detail </b-button>
      <b-button variant="secondary" v-on:click="goRefreshContainer()">
        Refresh
      </b-button>
    </b-button-group>
    <ContainerBtn
      :container_id="container.Id"
      :host_id="host_id"
      :container_state="container.State"
    ></ContainerBtn>
  </b-jumbotron>
</template>

<script>
import { mapActions } from "vuex";
import ContainerBtn from "@/components/docker/ContainerBtn";

export default {
  name: "Container",
  components: {
    ContainerBtn: ContainerBtn
  },
  props: ["container", "host_id"],

  data() {
    return {
      colors: {
        paused: "warning",
        restarting: "info",
        running: "success",
        dead: "danger",
        created: "primary",
        exited: "secondary"
      }
    };
  },
  computed: {
    is_on: function () {
      switch (this.container.State) {
        case "running":
        case "restarting":
          return true;
        default:
          return false;
      }
    }
  },
  methods: {
    ...mapActions(["executeHost"]),
    goDetail: function () {
      this.$router.push({
        name: "HostContainerDetail",
        params: {
          id: this.host_id,
          obj: this.container.Id,
          pre_container: this.container
        },
        props: true
      });
    },
    goRefreshContainer: function () {
      this.$parent.goRefreshFilters({ id: this.container.Id });
    }
  }
};
</script>
