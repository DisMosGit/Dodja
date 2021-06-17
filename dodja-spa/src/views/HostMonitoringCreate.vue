<template>
  <div>
    <b-container class="my-2 p-2 shadow-sm ">
      <b-form-group :label="$tc('description') | capitalize" description="">
        <b-form-input
          v-model="input.text"
          type="text"
          placeholder="text"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group :label="$tc('cron_rule') | capitalize" description="">
        <b-form-input
          v-model="input.cron_rule"
          type="text"
          placeholder="cron_rule"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group :label="$tc('priority') | capitalize" description="">
        <b-form-input
          v-model="input.priority"
          type="text"
          placeholder="priority"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group :label="$tc('condition') | capitalize" description="">
        <CodeTextarea
          ref="yaml-condition"
          default="action:\n\tcommand: api.ping\n\targs: {}\nexpected:\n\t- value: true\n\t  parameter: state\n\t  comparison: eq\n\t#- value: true\n\t  #parameter: state\n\t  #comparison: eq"
          mode="yaml"
        ></CodeTextarea>
      </b-form-group>
      <b-button-group>
        <b-button @click="tryCreate" variant="primary">
          {{ $t("create") | capitalize }}
        </b-button>
        <b-button @click="tryReset" variant="warning">
          {{ $t("reset") | capitalize }}
        </b-button>
      </b-button-group>
    </b-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import CodeTextarea from "@/components/CodeTextarea";
export default {
  name: "HostMonitoringCreate",
  components: {
    CodeTextarea
  },
  props: ["host_id"],
  data() {
    return {
      input: {
        text: "ping",
        cron_rule: "*/5 * * * *",
        priority: 0
      }
    };
  },
  computed: {
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
    ...mapActions(["createMonitoringTask"]),
    tryCreate() {
      this.createMonitoringTask({
        host_id: this.host_id,
        data: Object.assign({ condition: this.condition }, this.input)
      })
        .then(() => {
          this.$parent.goRefreshTaskList();
        })
        .catch(error => {
          console.log(error);
        });
    },
    tryReset() {
      this.input.text = "ping";
      this.input.cron_rule = "*/5 * * * *";
      this.condition =
        "- action:\n\tcommand: api.ping\n\targs: {}\n  expected:\n\tvalue: true\n\tparameter: state\n\tcomparison: eq\n#- action: ...";
    }
  }
};
</script>
