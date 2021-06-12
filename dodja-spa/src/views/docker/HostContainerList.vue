<template>
  <div>
    <h1>HostContainerList</h1>
    <b-button variant="success" v-on:click="goRefreshList()">
      Refresh list
    </b-button>
    <div class="row justify-content-md-center mx-0">
      <Container
        v-for="container in container_list"
        v-bind:key="container.Id"
        v-bind:container="container"
        v-bind:host_id="host_id"
      ></Container>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import Container from "@/components/docker/Container";

export default {
  name: "HostContainerList",
  props: ["host_id"],
  components: {
    Container
  },
  data() {
    return {
      container_list: null
    };
  },
  methods: {
    ...mapActions(["executeHost"]),
    goRefreshList() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.containers",
          args: {
            all: true
          }
        }
      })
        .then(response => {
          this.container_list = response.data.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    goRefreshFilters(filters) {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.containers",
          args: {
            all: true,
            filters: filters
          }
        }
      })
        .then(response => {
          this.container_list = this.container_list.map(
            obj => response.data.data.find(o => o.Id === obj.Id) || obj
          );
        })
        .catch(error => {
          console.log(error);
        });
    },
    goCreateContainer(args) {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.create_container",
          args: args
        }
      })
        .then(response => {
          console.log(response);
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  mounted() {
    console.log("mount_cl");
    this.goRefreshList();
  }
};
</script>
