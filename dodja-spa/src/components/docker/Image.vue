<template>
  <b-jumbotron border-variant="dark" class="col-md-auto m-1 p-1 shadow-sm">
    <h2>
      <b-badge>{{ image.Id | cut(7, 16) }}</b-badge>
      <b-badge variant="light">{{ image.Created | toDate("ms") }}</b-badge>
    </h2>
    <hr class="my-2" />
    <p class="text-break m-0" v-for="tag in image.RepoTags" v-bind:key="tag">
      {{ tag }}
    </p>
    <hr />
    <b-button-group>
      <b-button variant="primary" v-on:click="goDetail()">
        Detail
      </b-button>
      <b-button variant="danger" v-on:click="goStop()">
        Pull
      </b-button>
      <b-button variant="info" v-on:click="goStart()">
        Tag
      </b-button>
    </b-button-group>
  </b-jumbotron>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Image",
  props: ["image", "host_id"],
  methods: {
    ...mapActions(["executeHost"]),
    goTag: function() {
      // TODO:
      // this.$router.push({
      //   name: "HostContainerDetail",
      //   params: {
      //     id: this.host_id,
      //     obj: this.container.Id,
      //     pre_container: this.container
      //   },
      //   props: true
      // });
    },
    goPush: function() {
      // TODO:
      // this.executeHost({
      //   id: this.host_id,
      //   data: {
      //     command: "api.remove_image",
      //     args: { container: this.image.Id }
      //   }
      // }).then(() => {
      //   this.$router.push({
      //     name: "HostDocker",
      //     params: { id: this.host.id }
      //   });
      // });
    }
  }
};
</script>
