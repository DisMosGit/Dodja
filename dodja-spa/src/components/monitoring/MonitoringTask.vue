<template>
  <b-jumbotron border-variant="dark" class="col-md-auto m-1 p-1 shadow-sm">
    <h2 class="text-break">
      <b-badge :variant="status">
        {{ task.next_launch | toDate("time") }}
      </b-badge>
      {{ task.text }}
      <b-badge variant="light">{{ task.priority }}</b-badge>
    </h2>
    <p class="text-break m-0">rule: {{ task.cron_rule }}</p>
    <p class="text-break m-0">
      last launch: {{ task.last_launch | toDate("locl") }}
    </p>
    <hr class="my-2" />
    <p>{{ task.condition.action.command }}</p>
    <p
      class="text-break m-0"
      v-for="(expected, index) in task.condition.expected"
      v-bind:key="index"
    >
      {{ expected.parameter }}
    </p>
    <hr class="my-2" />
    <b-button-group>
      <b-button
        variant="primary"
        :to="{
          name: 'HostMonitoringTask',
          params: { id: host_id, task: task.id }
        }"
      >
        Detail
      </b-button>
      <b-button variant="secondary" v-on:click="goRefreshTask()">
        Refresh
      </b-button>
      <b-button
        :variant="is_on ? 'warning' : 'success'"
        v-on:click="switchStatus()"
      >
        {{ is_on ? "Stop" : "Start" }}
      </b-button>
    </b-button-group>
  </b-jumbotron>
</template>

<script>
export default {
  name: "MonitoringTask",
  props: ["task", "host_id"],
  computed: {
    status: function() {
      if (this.task.is_lock) {
        return "danger";
      } else {
        if (this.task.is_active) {
          return "success";
        } else {
          return "warning";
        }
      }
    },
    is_on: function() {
      if (this.task.is_lock) {
        return false;
      } else {
        if (this.task.is_active) {
          return true;
        } else {
          return false;
        }
      }
    }
  },
  methods: {
    goRefreshTask: function() {
      this.$parent.goRefreshTaskList();
    },
    switchStatus: function() {
      this.$emit("switch", this.task.id, {
        is_active: !this.task.is_active,
        is_lock: false
      });
    }
  }
};
</script>
