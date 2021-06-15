<template>
  <b-container class="my-2 p-2 shadow-sm ">
    <h2 class="text-center">
      {{ $tc("edit", 2) | capitalize }}
      <b-badge @click="goRefresh">
        <b-icon-arrow-repeat></b-icon-arrow-repeat>
      </b-badge>
    </h2>
    <b-form-group
      id="input-group-1"
      :label="$tc('title') | capitalize"
      label-for="title"
      description=""
    >
      <b-form-input
        id="title"
        v-model="host_edited.title"
        type="text"
        placeholder="Title"
        required
      ></b-form-input>
    </b-form-group>

    <b-form-group
      id="input-group-2"
      :label="$tc('description') | capitalize"
      label-for="description"
      description=""
    >
      <b-form-input
        id="description"
        v-model="host_edited.description"
        type="text"
        placeholder="description"
        required
      ></b-form-input>
    </b-form-group>

    <b-form-group
      id="input-group-3"
      :label="$tc('credentials') | capitalize"
      label-for="credentials"
      description=""
    >
      <CodeTextarea
        ref="yaml-credentials"
        default="key: value\n"
        mode="yaml"
      ></CodeTextarea>
    </b-form-group>
    <b-form-group
      id="input-group-4"
      :label="$tc('settings') | capitalize"
      label-for="settings"
      description=""
    >
      <CodeTextarea
        ref="yaml-settings"
        default="key: value\n"
        mode="yaml"
      ></CodeTextarea>
    </b-form-group>
    <b-button-group>
      <b-button @click="tryUpdate" variant="primary">
        {{ $t("update") | capitalize }} {{ $tc("host") | capitalize }}
      </b-button>
      <b-button @click="tryReset" variant="warning">
        {{ $t("reset") | capitalize }}
      </b-button>
      <b-button @click="tryDelete" variant="danger">
        {{ $t("delete") | capitalize }} {{ $tc("host") | capitalize }}
      </b-button>
    </b-button-group>
  </b-container>
</template>

<script>
import { mapActions, mapMutations } from "vuex";
import CodeTextarea from "@/components/CodeTextarea";

export default {
  name: "HostEdit",
  components: {
    CodeTextarea
  },
  model: {
    prop: "host",
    event: "change"
  },
  props: {
    host: Object,
    host_id: String
  },
  data() {
    return {
      host_edited: {}
    };
  },
  watch: {
    host: function() {
      this.host_edited = this.host;
      this.updateTextarea();
    }
  },
  computed: {
    settings: {
      get: function() {
        return this.$refs["yaml-settings"].text;
      },
      set: function(value) {
        this.$refs["yaml-settings"].editText(value);
      }
    },
    credentials: {
      get: function() {
        return this.$refs["yaml-credentials"].text;
      },
      set: function(value) {
        this.$refs["yaml-credentials"].editText(value);
      }
    }
  },
  methods: {
    ...mapActions(["updateHost", "deleteHost"]),
    ...mapMutations(["setMsg"]),
    tryUpdate() {
      if (this.host_edited.title == "" || false) {
        this.setMsg("Введите данные");
      } else {
        this.updateHost({
          id: this.host_id,
          data: {
            title: this.host_edited.title,
            description: this.host_edited.description,
            credentials: this.credentials,
            settings: this.settings
          }
        })
          .then(response => {
            this.goRefresh();
            this.setMsg("Обновлен, " + response.data.title);
          })
          .catch(error => {
            this.setMsg("Введите данные: " + JSON.stringify(error.data.detail));
          });
      }
    },
    tryDelete() {
      this.deleteHost({
        id: this.host_id
      })
        .then(response => {
          this.$router.push({ name: "HostList" });
          this.setMsg("Удален: " + this.host.title + response.statusText);
        })
        .catch(error => {
          this.setMsg("Введите данные: " + JSON.stringify(error.data.detail));
        });
    },
    updateTextarea: function() {
      this.credentials = this.host_edited.credentials;
      this.settings = this.host_edited.settings;
    },
    goRefresh: function() {
      this.$parent.goRefreshHost();
    },
    tryReset() {
      this.goRefresh();
    }
  },
  mounted() {
    this.host_edited = this.host;
    this.updateTextarea();
  }
};
</script>
