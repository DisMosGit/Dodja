<template>
  <b-container>
    <h1 class="text-center">
      {{ $tc("create") | capitalize }} {{ $tc("host", 1) }}
    </h1>
    <b-form @submit="tryCreate" @reset="tryReset" class="m-2">
      <b-form-group
        id="input-group-1"
        label="title:"
        label-for="title"
        description=""
      >
        <b-form-input
          id="title"
          v-model="title"
          type="text"
          placeholder="Title"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="description:"
        label-for="description"
        description=""
      >
        <b-form-input
          id="description"
          v-model="description"
          type="text"
          placeholder="description"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-3"
        label="credentials:"
        label-for="credentials"
        description=""
      >
        <YamlTextarea
          ref="yaml-credentials"
          default="base_url: unix://var/run/docker.sock\nuse_ssh_client: false"
        ></YamlTextarea>
      </b-form-group>
      <b-form-group
        id="input-group-4"
        label="settings:"
        label-for="settings"
        description=""
      >
        <YamlTextarea
          ref="yaml-settings"
          default="default_permissions: 777"
        ></YamlTextarea>
      </b-form-group>
      <b-button-group>
        <b-button type="submit" variant="primary">
          {{ $tc("create") | capitalize }}
          {{ $tc("host", 1) }}
        </b-button>
        <b-button type="reset" variant="warning">
          {{ $tc("reset", 1) | capitalize }}
        </b-button>
      </b-button-group>
    </b-form>
  </b-container>
</template>

<script>
import { mapActions, mapMutations } from "vuex";
import YamlTextarea from "@/components/YamlTextarea";

export default {
  name: "HostCreate",
  components: {
    YamlTextarea
  },
  data() {
    return {
      title: "",
      description: ""
    };
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
    ...mapActions(["createHost"]),
    ...mapMutations(["setMsg"]),
    tryCreate(event) {
      event.preventDefault();
      console.log(
        this.title,
        this.description,
        this.credentials,
        this.settings
      );
      if (this.title == "" || false) {
        this.setMsg("Введите данные");
      } else {
        this.createHost({
          title: this.title,
          description: this.description,
          credentials: this.credentials,
          settings: this.settings
        })
          .then(response => {
            this.$router.push({
              name: "HostDetail",
              params: { id: response.data.id }
            });
            this.setMsg("Создан, " + response.data.title);
          })
          .catch(error => {
            this.setMsg("e Введите данные: " + JSON.stringify(error.data));
          });
      }
    },
    tryReset(event) {
      event.preventDefault();
      this.credentials;
      this.settings;
    }
  }
};
</script>
