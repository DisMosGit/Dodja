<template>
  <b-jumbotron border-variant="dark" class="col-md-auto m-1 p-1">
    <h2>
      <b-badge :variant="this.colors[container.State]">{{
        container.Id | cut(0, 10)
      }}</b-badge>
      {{ container.Names | dockerNames }}
      <b-badge variant="light">{{ container.Created | toDate("ms") }}</b-badge>
    </h2>
    <p>{{ container.State }}: {{ container.Status }}</p>
    <p>{{ container.Image }}: {{ container.ImageID | cut(0, 20) }}</p>
    <hr class="my-2" />
    <p>
      {{ container.Ports | dockerPorts }}
    </p>
    <p>
      {{ container.Mounts | dockerMounts }}
    </p>
    <b-button-group>
      <b-button variant="primary" v-on:click="goDetail()">
        Detail
      </b-button>
      <b-button v-if="is_on" variant="outline-danger" v-on:click="goRefresh()">
        goRefresh
      </b-button>
      <b-button v-if="is_on" variant="warning" v-on:click="goRestart()">
        Restart
      </b-button>
      <b-button v-if="is_on" variant="danger" v-on:click="goStop()">
        Stop
      </b-button>
      <b-button v-if="!is_on" variant="success" v-on:click="goStart()">
        Start
      </b-button>
    </b-button-group>
  </b-jumbotron>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Image",
  props: ["image", "host_id"],

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
    is_on: function() {
      switch (this.container.State) {
        case "paused":
        case "dead":
        case "created":
        case "exited":
          return false;
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
    goDetail: function() {
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
    goStop: function() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.stop",
          args: { container: this.container.Id }
        }
      }).then(() => {
        this.goRefresh();
      });
    },
    goRestart: function() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.restart",
          args: { container: this.container.Id }
        }
      }).then(() => {
        this.goRefresh();
      });
    },
    goStart: function() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.start",
          args: { container: this.container.Id }
        }
      }).then(() => {
        this.goRefresh();
      });
    },
    goRefresh: function() {
      this.$parent.goRefreshFilters({ id: this.container.Id });
    }
  }
};
</script>
