<template>
  <b-dropdown
    text="Change state"
    class="mx-2"
    dropup
    :variant="is_on ? 'outline-danger' : 'outline-success'"
  >
    <b-dropdown-item-btn
      v-show="is_on"
      variant="danger"
      v-on:click="goSimpleCommand('api.stop')"
    >
      Stop
    </b-dropdown-item-btn>
    <b-dropdown-item
      v-show="is_on"
      variant="warning"
      v-on:click="goSimpleCommand('api.restart')"
    >
      Restart
    </b-dropdown-item>
    <b-dropdown-item
      v-show="is_on"
      variant="warning"
      v-on:click="goSimpleCommand('api.pause')"
    >
      Pause
    </b-dropdown-item>
    <b-dropdown-item
      v-show="is_pause"
      variant="success"
      v-on:click="goSimpleCommand('api.unpause')"
    >
      Unpause
    </b-dropdown-item>
    <b-dropdown-item
      v-show="!is_on && !is_pause"
      variant="success"
      v-on:click="goSimpleCommand('api.start')"
    >
      Start
    </b-dropdown-item>
  </b-dropdown>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "ContainerBtn",
  props: ["container_id", "host_id", "container_state"],

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
      simple_commands: {
        pause: "api.pause",
        unpause: "api.unpause",
        start: "api.start",
        stop: "api.stop",
        restart: "api.restart"
      }
    };
  },
  computed: {
    is_on: function() {
      switch (this.container_state) {
        case "running":
        case "restarting":
          return true;
        default:
          return false;
      }
    },
    is_pause: function() {
      switch (this.container_state) {
        case "paused":
          return true;
        default:
          return false;
      }
    }
  },

  methods: {
    ...mapActions(["executeHost"]),
    goSimpleCommand: function(command) {
      console.log("run", command);
      this.executeHost({
        id: this.host_id,
        data: {
          command: command,
          args: { container: this.container_id }
        }
      }).then(() => {
        this.$parent.goRefreshContainer();
      });
    }
  }
};
</script>
