<template>
  <b-card>
    <b-card-title>
      <b-badge :variant="status">
        {{ seconds }}
      </b-badge>
      {{ log.date_created | toDate("locl") }}
    </b-card-title>
    <b-card-sub-title class="mb-2">
      {{ log.is_passed ? "Passed" : "Failed" }}
    </b-card-sub-title>
    <b-card-text class="text-justify text-wrap text-break">
      <LogCheck
        v-for="result in log.result"
        v-bind:key="result.parameter"
        v-bind:result="result"
      ></LogCheck>
    </b-card-text>
    <b-button-group size="sm">
      <b-button variant="danger" v-on:click="tryDelete()">
        Remove
      </b-button>
    </b-button-group>
  </b-card>
</template>

<script>
import LogCheck from "@/components/monitoring/LogCheck";
export default {
  name: "MonitoringTaskLog",
  components: {
    LogCheck
  },
  props: ["log", "host_id"],
  computed: {
    status: function() {
      if (this.log.is_runtime_error) {
        return "danger";
      } else {
        if (this.log.is_passed) {
          return "success";
        } else {
          return "warning";
        }
      }
    },
    seconds: function() {
      var parts = this.log.duration.split(":");
      return (
        Number(parts[0]) * 60 * 60 + Number(parts[1]) * 60 + Number(parts[2])
      );
    }
  },
  methods: {
    tryDelete: function() {
      this.$emit("remove", this.log.id);
    }
  }
};
// <template>
//   <b-jumbotron border-variant="dark" class="col-md-auto m-1 p-1 shadow-sm">
//     <h2 class="text-break">
//       <b-badge :variant="status">
//         {{ task.duration | toDate("time") }}
//       </b-badge>
//       {{ task.text }}
//       <b-badge variant="light">{{ task.priority }}</b-badge>
//     </h2>
//     <p class="text-break m-0">rule: {{ task.cron_rule }}</p>
//     <p class="text-break m-0">last launch: {{ task.last_launch }}</p>
//     <hr class="my-2" />
//     <p class="text-break m-0">command: {{ task.action.command }}</p>
//     <hr class="my-2" />
//     <b-button-group>
//       <b-button variant="secondary" v-on:click="tryDelete()">
//         Refresh
//       </b-button>
//     </b-button-group>
//   </b-jumbotron>
// </template>
</script>
