<template>
  <div class="border">
    <b-form @submit="tryExecute" @reset="onReset">
      <ReadTextarea ref="read-result"></ReadTextarea>
      <div class="input-group">
        <input
          class="form-control"
          placeholder="Custom Command"
          v-model="input.command"
        />
        <div class="input-group-append">
          <button type="submit" class="btn btn-outline-primary">
            Run command
          </button>
        </div>
      </div>
      <YamlTextarea
        ref="yaml-to-json"
        default="args:\n\tkey: value"
      ></YamlTextarea>
      <div class="input-group input-group-sm background-white" title="Options">
        <div class="input-group-prepend">
          <div class="input-group-text">
            Get list
            <input
              type="checkbox"
              v-model="input.is_list"
              aria-label="Get list"
              class="ml-1"
            />
          </div>
        </div>
        <div class="input-group-prepend">
          <div class="input-group-text">
            Run in background
            <input
              v-model="input.is_background"
              type="checkbox"
              aria-label="Run in background"
              class="ml-1"
            />
          </div>
        </div>
        <div class="input-group-prepend">
          <div class="input-group-text">
            Get full response data
            <input
              v-model="input.is_full_response"
              type="checkbox"
              aria-label="Get full response data"
              class="ml-1"
            />
          </div>
        </div>
        <div class="input-group-prepend">
          <div class="input-group-text">
            Get raw result
            <input
              v-model="input.is_raw_result"
              type="checkbox"
              aria-label="Get raw result"
              class="ml-1"
            />
          </div>
          <b-button type="reset" variant="btn btn-outline-danger"
            >Reset form</b-button
          >
          <b-button variant="btn btn-outline-warning" @click="clearText"
            >Clear result</b-button
          >
        </div>
      </div>
    </b-form>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import YamlTextarea from "@/components/YamlTextarea";
import ReadTextarea from "@/components/ReadTextarea";

export default {
  name: "HostManager",
  props: ["host_id"],
  components: {
    YamlTextarea,
    ReadTextarea
  },
  data() {
    return {
      input: {
        command: "",
        is_background: false,
        is_list: false,
        is_full_response: false,
        is_raw_result: false
      }
    };
  },
  methods: {
    ...mapActions(["executeHost"]),
    tryExecute(event) {
      event.preventDefault();
      console.log("arg", this.$refs["yaml-to-json"].text);
      event.preventDefault();
      this.executeHost({
        id: this.host_id,
        data: {
          command: this.input.command,
          args: this.$refs["yaml-to-json"].text.args
        }
      })
        .then(response => {
          if (this.input.is_full_response) {
            this.$refs["read-result"].addText(response.data);
          } else {
            this.$refs["read-result"].addText(response.data.data);
          }
        })
        .catch(error => {
          if (this.input.is_full_response) {
            this.$refs["read-result"].addText(error.data);
          } else {
            this.$refs["read-result"].addText(error.data.detail);
          }
        });
    },
    clearText() {
      this.$refs["read-result"].deleteText();
    },
    onReset(event) {
      event.preventDefault();
      this.input.command = "";
      this.input.is_list = false;
      this.input.is_background = false;
      this.$refs["yaml-to-json"].text = null;
    }
  }
};
</script>
