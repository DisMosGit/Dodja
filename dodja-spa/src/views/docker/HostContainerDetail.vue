<template>
  <div v-if="container">
    <h1>HostContainerList</h1>
    <h2>
      {{ container.Id.substring(0, 10) }}
      {{ container.Name.substring(1) }}
      <b-badge :variant="this.colors[container.State.Status]">
        {{ container.State.Status }}
      </b-badge>
      <b-badge variant="light">{{ container.Created | toDate }}</b-badge>
    </h2>
    <hr class="my-2" />
    <p>image: {{ container.Image }}</p>
    <p>restarts: {{ container.RestartCount }}</p>
    <p
      class="text-break m-0"
      v-for="(mount, key) in container.Mounts"
      v-bind:key="key"
    >
      {{ mount.Source }}->{{ mount.Destination }}:{{ mount.Mode }}
    </p>
    <b-form>
      <b-form-textarea
        id="input-cmd-text"
        v-model="cmd_text"
        plaintext
        class="border rounded border-secondary"
      ></b-form-textarea>
      <b-form-group id="input-cmd-group" label-for="input-cmd" class="border">
        <b-form-input
          id="input-cmd"
          v-model="cmd"
          placeholder="> Enter cmd"
          class="mt-1"
        ></b-form-input>
      </b-form-group>
    </b-form>
    <b-button variant="secondary" v-on:click="clearText()">
      Clear console
    </b-button>
    <b-button-group>
      <ContainerBtn
        :container_id="container.Id"
        :host_id="host_id"
        :container_state="container.State.Status"
      ></ContainerBtn>
      <b-button v-if="is_on" variant="warning" v-on:click="goRestart()">
        Restart
      </b-button>

      <b-button variant="info" v-on:click="goStats()"> Stats </b-button>
      <b-button variant="info" v-on:click="goTop()"> Top </b-button>
      <b-button variant="info" v-on:click="goLogs()"> Logs </b-button>
      <b-button class="mx-2" variant="warning" v-on:click="goKill()">
        Kill
      </b-button>
      <b-button class="mx-2" variant="danger" v-on:click="goDelete()">
        Delete
      </b-button>
    </b-button-group>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import ContainerBtn from "@/components/docker/ContainerBtn";

export default {
  name: "HostContainerDetail",
  components: {
    ContainerBtn: ContainerBtn
  },
  computed: {
    container_id: function () {
      return this.$route.params.obj;
    },
    host_id: function () {
      return this.$route.params.id;
    },
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
  data() {
    return {
      colors: {
        paused: "warning",
        restarting: "info",
        running: "success",
        dead: "danger",
        created: "primary",
        exited: "secondary"
      },
      cmd: "",
      cmd_text: "",
      container: null,
      image: {}
    };
  },
  methods: {
    ...mapActions(["executeHost"]),
    goContainerDeatil() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.inspect_container",
          args: { container: this.container_id }
        }
      })
        .then((response) => {
          this.container = response.data.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    goImage() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.inspect_image",
          args: { image: this.container.Image }
        }
      })
        .then((response) => {
          this.image = response.data.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    goRefreshContainer: function () {
      this.goContainerDeatil();
    },
    goKill: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.kill",
          args: { container: this.container_id }
        }
      }).then(() => {
        this.goRefreshContainer();
      });
    },
    goStats: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.stats",
          args: { container: this.container_id, stream: false }
        }
      }).then((response) => {
        this.cmd_text += JSON.stringify({
          cpu: response.data.data.cpu_stats.online_cpus,
          memory: response.data.data.memory_stats.usage,
          network: response.data.data.networks
        });
        this.cmd_text += "\n";
      });
    },
    goTop: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.top",
          args: { container: this.container_id }
        }
      }).then((response) => {
        this.cmd_text += JSON.stringify(response.data.data);
        this.cmd_text += "\n";
      });
    },
    goLogs: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.logs",
          args: { container: this.container_id }
        }
      }).then((response) => {
        this.cmd_text += JSON.stringify(response.data.data);
        this.cmd_text += "\n";
      });
    },
    clearText: function () {
      this.cmd_text = "";
    },
    // goRename: function () {
    //   this.executeHost({
    //     id: this.host_id,
    //     data: {
    //       command: "api.logs",
    //       args: { container: this.container_id }
    //     }
    //   }).then(() => {
    //     console.log("rename");
    //   });
    // },
    goDelete: function (volumes, link, force) {
      console.log(volumes, link, force);
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.remove_container",
          args: { container: this.container_id }
        }
      }).then(() => {
        this.$router.push({
          name: "HostDockerContainer",
          params: { id: this.host_id }
        });
      });
    }
  },
  mounted() {
    this.goRefreshContainer();
  }
};
</script>
