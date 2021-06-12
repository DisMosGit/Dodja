<template>
  <div>
    <h2>
      HostDocker<DockerInfo
        v-if="ping"
        v-bind:version="version"
        v-bind:info="info"
      />
    </h2>
    <div v-if="ping">
      <router-view v-bind:host_id="host_id" />
      <div>
        <input
          type="checkbox"
          name="show"
          v-model="showManager"
          placeholder="show"
        />
        <HostManager v-bind:host_id="host_id" v-show="showManager" />
      </div>
    </div>
    <div v-else>
      {{ $tc("docker", 1) | capitalize }} {{ $tc("loading", 1) | capitalize }}
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import HostManager from "./docker/HostManager.vue";
import DockerInfo from "@/components/docker/DockerInfo";

export default {
  name: "HostDocker",
  components: {
    HostManager,
    DockerInfo
  },
  props: ["host_id"],
  data() {
    return {
      ping: null,
      info: null,
      version: null,
      showManager: true
    };
  },
  methods: {
    ...mapActions(["executeHost", "getHostDetail"]),
    goDockerInfo() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.info",
          args: {}
        }
      }).then(response => {
        this.info = response.data.data;
      });
    },
    goDockerPing() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.ping",
          args: {}
        }
      }).then(response => {
        this.ping = response.data.data.state;
      });
    },
    goDockerVersion() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.version",
          args: {}
        }
      }).then(response => {
        this.version = response.data.data;
      });
    }
  },
  mounted() {
    this.goDockerPing();
    this.goDockerVersion();
    this.goDockerInfo();
  }
};
</script>
