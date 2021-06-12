<template>
  <b-container>
    <div v-if="host">
      <h1 class="text-center">{{ host.title }}</h1>
      <b-button @click="goRefreshHost" variant="primary"
        >{{ $t("refresh") | capitalize }} {{ $tc("host") }}</b-button
      >
      <DockerBtn class="mx-2" v-bind:host_id="host_id" />
      <router-view
        v-if="$route.name != 'HostDetail'"
        v-bind:host_id="host_id"
      />
      <div v-else>
        <HostEdit v-model="host" v-bind:host_id="host_id"></HostEdit>
        <HostAccess
          v-bind:settings="host.settings"
          v-bind:host_id="host_id"
        ></HostAccess>
      </div>
    </div>
    <div v-else>
      <h1 class="text-center">{{ $tc("loading", 1) | capitalize }}...</h1>
    </div>
  </b-container>
</template>

<script>
import { mapActions, mapMutations } from "vuex";
import DockerBtn from "@/components/DockerBtn";
import HostEdit from "@/views/HostEdit";
import HostAccess from "@/views/HostAccess";

export default {
  name: "HostDetail",
  components: {
    DockerBtn,
    HostEdit,
    HostAccess
  },
  data() {
    return {
      host: null
    };
  },
  computed: {
    host_id: function() {
      return this.$route.params.id;
    }
  },
  methods: {
    ...mapActions(["getHostDetail"]),
    ...mapMutations(["setMsg"]),
    goRefreshHost: function() {
      return this.getHostDetail({ id: this.host_id })
        .then(response => {
          this.host = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    updateHostData: function(host) {
      this.host = host;
    }
  },
  mounted() {
    this.goRefreshHost();
  }
};
</script>
