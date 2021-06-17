<template>
  <div>
    <b-container class="my-2 p-2 shadow-sm ">
      <p>
        Last launch: {{ task.last_launch | toDate("locl") }}
        <b-badge :variant="status">
          {{ is_on ? "On" : "Off" }}
        </b-badge>
      </p>
      <p>Next launch: {{ task.next_launch | toDate("locl") }}</p>
      <b-form-group :label="$tc('description') | capitalize" description="">
        <b-form-input
          v-model="task.text"
          type="text"
          placeholder="text"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group :label="$tc('cron_rule') | capitalize" description="">
        <b-form-input
          v-model="task.cron_rule"
          type="text"
          placeholder="cron_rule"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group :label="$tc('priority') | capitalize" description="">
        <b-form-input
          v-model="task.priority"
          type="text"
          placeholder="priority"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group :label="$tc('condition') | capitalize" description="">
        <CodeTextarea
          ref="yaml-condition"
          default=""
          mode="yaml"
        ></CodeTextarea>
      </b-form-group>
      <b-button-group>
        <b-button @click="tryUpdateTask" variant="success">
          {{ $t("update") | capitalize }}
        </b-button>
        <b-button @click="goRefreshTaskSingle" variant="secondary">
          {{ $t("refresh") | capitalize }}
        </b-button>
        <b-button @click="tryDeleteTask" variant="danger">
          {{ $t("delete") | capitalize }}
        </b-button>
        <b-button
          :variant="is_on ? 'warning' : 'success'"
          v-on:click="switchStatus()"
        >
          {{ is_on ? "Stop" : "Start" }}
        </b-button>
      </b-button-group>
    </b-container>
    <div>
      <MonitoringTaskLog
        v-for="log in log_list"
        v-bind:key="log.id"
        v-bind:log="log"
        v-bind:host_id="host_id"
        @remove="tryDeleteLog"
      ></MonitoringTaskLog>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import MonitoringTaskLog from "@/components/monitoring/MonitoringTaskLog";
import CodeTextarea from "@/components/CodeTextarea";
export default {
  name: "HostMonitoring",
  components: {
    MonitoringTaskLog,
    CodeTextarea
  },
  props: ["host_id"],
  data() {
    return { task: {}, log_list: [], first_update: false };
  },
  computed: {
    task_id: function() {
      return this.$route.params.task;
    },
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
    },
    condition: {
      get: function() {
        return this.$refs["yaml-condition"].text;
      },
      set: function(value) {
        this.$refs["yaml-condition"].editText(value);
      }
    }
  },
  methods: {
    ...mapActions([
      "getMonitoringTaskDetail",
      "updateMonitoringTask",
      "deleteMonitoringTask",
      "getMonitoringTaskLogList",
      "deleteMonitoringTaskLog"
    ]),
    goRefreshTaskSingle() {
      this.getMonitoringTaskDetail({
        host_id: this.host_id,
        id: this.task_id
      })
        .then(response => {
          this.task = response.data;
          this.condition = this.task.condition;
        })
        .catch(error => {
          console.log(error);
        });
      this.getMonitoringTaskLogList({
        host_id: this.host_id,
        id: this.task_id
      })
        .then(response => {
          this.log_list = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    tryUpdateTask() {
      this.updateMonitoringTask({
        host_id: this.host_id,
        id: this.task_id,
        data: Object.assign(this.task, { condition: this.condition })
      })
        .then(response => {
          this.task = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    tryDeleteTask() {
      this.deleteMonitoringTask({
        host_id: this.host_id,
        id: this.task_id
      })
        .then(() => {
          this.$router.push({
            name: "HostMonitoring",
            params: { host_id: this.host_id }
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    tryDeleteLog(id) {
      this.log_list.splice(
        this.log_list.indexOf(x => x.id == id),
        1
      );
      this.deleteMonitoringTaskLog({
        host_id: this.host_id,
        id: this.task_id,
        log_id: id
      })
        .then(() => {})
        .catch(error => {
          console.log(error);
        });
    },
    switchStatus: function() {
      this.updateMonitoringTask({
        host_id: this.host_id,
        id: this.task_id,
        data: { is_active: !this.task.is_active, is_lock: false }
      })
        .then(response => {
          this.task = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  mounted() {
    this.goRefreshTaskSingle();
  },
  updated() {}
};
</script>
