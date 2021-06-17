<template>
  <div>
    <div class="p-2">
      <b-button class="mx-auto" @click="switchAddMode" variant="primary">
        {{ add_mode ? $tc("close") : $tc("add") | capitalize }}
      </b-button>
      <div v-show="add_mode">
        <HostMonitoringCreate v-bind:host_id="host_id"></HostMonitoringCreate>
      </div>
    </div>
    <div class="row justify-content-md-center mx-0">
      <MonitoringTask
        v-for="task in task_list"
        v-bind:key="task.id"
        v-bind:task="task"
        v-bind:host_id="host_id"
        @switch="tryUpdateTask"
      ></MonitoringTask>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import MonitoringTask from "@/components/monitoring/MonitoringTask";
import HostMonitoringCreate from "@/views/HostMonitoringCreate";

export default {
  name: "HostMonitoring",
  components: {
    MonitoringTask,
    HostMonitoringCreate
  },
  props: ["host_id"],
  data() {
    return { task_list: [], add_mode: true };
  },
  methods: {
    ...mapActions([
      "getMonitoringTaskList",
      "getMonitoringTaskDetail",
      "updateMonitoringTask"
    ]),
    goRefreshTaskList: function() {
      this.getMonitoringTaskList({
        host_id: this.host_id
      })
        .then(response => {
          this.task_list = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    goRefreshTaskSingle: function(id) {
      this.getMonitoringTaskDetail({
        host_id: this.host_id,
        id: id
      })
        .then(response => {
          this.task_list.every(function(element, index) {
            if (element.id == response.data.id) {
              this.task_list[index] = response.data;
              return false;
            } else return true;
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    tryUpdateTask: function(id, data) {
      this.updateMonitoringTask({
        host_id: this.host_id,
        id: id,
        data: data
      })
        .then(() => {
          this.goRefreshTaskList();
        })
        .catch(error => {
          console.log(error);
        });
    },
    switchAddMode: function() {
      this.add_mode = !this.add_mode;
    }
  },
  mounted() {
    this.goRefreshTaskList();
  }
};
</script>
