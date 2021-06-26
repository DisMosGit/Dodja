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
    <!-- <p>
      {{ container.Ports | dockerPorts }}
    </p>
    <p>
      {{ container.Mounts | dockerMounts }}
    </p> -->
    <b-form>
      <b-form-textarea
        id="input-cmd-text"
        v-model="cmd_text"
        plaintext
        class="border rounded border-secondary"
      ></b-form-textarea>
      <b-form-group
        id="input-cmd-group"
        label-for="input-cmd"
        class="border"
        description="Type a command."
      >
        <b-form-input
          id="input-cmd"
          v-model="cmd"
          placeholder="> Enter cmd"
          class="mt-1"
        ></b-form-input>
      </b-form-group>
    </b-form>
    <b-button-group>
      <b-button
        v-if="is_on"
        variant="outline-danger"
        v-on:click="goRefreshContainer()"
      >
        goRefresh
      </b-button>
      <b-button v-if="is_on" variant="warning" v-on:click="goRestart()">
        Restart
      </b-button>
    </b-button-group>
    <ContainerBtn
      :container_id="container.Id"
      :host_id="host_id"
      :container_state="container.State.Status"
    ></ContainerBtn>
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
      container: {},
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
          console.log(this.container);
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
    getYaml: function (data) {
      console.log("data", data);
    },
    goKill: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.kill",
          args: { container: this.container.Id }
        }
      }).then(() => {
        console.log("rename");
      });
    },
    goStats: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.stats",
          args: { container: this.container.Id }
        }
      }).then(() => {
        console.log("rename");
      });
    },
    goTop: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.top",
          args: { container: this.container.Id }
        }
      }).then(() => {
        console.log("rename");
      });
    },
    goLogs: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.logs",
          args: { container: this.container.Id }
        }
      }).then(() => {
        console.log("rename");
      });
    },
    goRename: function () {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.logs",
          args: { container: this.container.Id }
        }
      }).then(() => {
        console.log("rename");
      });
    },
    goRemoveMe: function (volumes, link, force) {
      console.log(volumes, link, force);
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.remove_container",
          args: { container: this.container.Id }
        }
      }).then(() => {
        console.log("rename");
      });
    }
  },
  mounted() {
    this.goRefreshContainer();
    console.log("hio", this.container);
  }
};
</script>
