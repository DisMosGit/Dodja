<template>
  <div>
    <h1 class="text-center">
      {{ $tc("host", 2) | capitalize
      }}<HintBtn hint_key="ru_host_list"></HintBtn>
    </h1>
    <div class="d-flex justify-content-center">
      <b-button variant="success" v-on:click="goCreate()">
        {{ $tc("add") | capitalize }}
      </b-button>
    </div>
    <div class="row justify-content-md-center mx-0">
      <Host
        v-for="host in hosts"
        v-bind:key="host.id"
        v-bind:host="host"
      ></Host>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import Host from "@/components/Host";

export default {
  name: "HostList",
  components: {
    Host
  },
  data() {
    return {
      hosts: null,
      actions: []
    };
  },
  computed: {
    ...mapGetters(["auth", "user", "message"])
  },
  methods: {
    ...mapActions(["getHostList"]),
    ...mapMutations(["setMsg"]),
    goCreate: function () {
      this.$router.push({ name: "HostCreate" });
    }
  },
  mounted() {
    this.getHostList({})
      .then((response) => {
        console.log(response);
        this.hosts = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  }
};
</script>
