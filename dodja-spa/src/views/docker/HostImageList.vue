<template>
  <div>
    <h1>HostImageList</h1>
    <b-button variant="success" v-on:click="goRefreshImageList()">
      Refresh list
    </b-button>
    <div class="row justify-content-md-center mx-0">
      <DockerImage
        v-for="image in image_list"
        v-bind:key="image.Id"
        v-bind:image="image"
        v-bind:host_id="host_id"
      ></DockerImage>
    </div>
    <b-form inline class="container m-2 p-1 shadow">
      <span>Pull Image:</span>
      <b-form-input
        class="m-2"
        placeholder="Repo"
        v-model="pull.repository"
      ></b-form-input>
      <b-form-input
        class="m-2"
        placeholder="Tag"
        v-model="pull.tag"
      ></b-form-input>

      <b-button variant="success" @click="tryPull">Pull</b-button>
    </b-form>
    <div class="container m-2 p-1 shadow">
      <h3>Build Image</h3>
      <label>Type a dockerfile text</label>
      <CodeTextarea
        ref="build-text"
        default="FROM image:version\nENTRYPOINT"
        mode="dockerfile"
      ></CodeTextarea>
      <hr />
      <label>Type build parameters</label>
      <CodeTextarea
        ref="build-args"
        default='tag: "example:version"\nnocache: false'
        mode="yaml"
      ></CodeTextarea>
      <hr />
      <label>Build result</label>
      <CodeTextarea
        ref="build-result"
        default=""
        :is_read="true"
        mode="javascript"
      ></CodeTextarea>
      <b-button-group>
        <b-button @click="tryBuild" variant="success">
          {{ $tc("build") | capitalize }} {{ $tc("image") | capitalize }}
        </b-button>
        <b-button @click="tryReset" variant="warning">
          {{ $tc("reset") | capitalize }}
        </b-button>
      </b-button-group>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import Image from "@/components/docker/Image";
import CodeTextarea from "@/components/CodeTextarea";

export default {
  name: "HostImageList",
  props: ["host_id"],
  components: {
    CodeTextarea,
    DockerImage: Image
  },
  data() {
    return {
      image_list: null,
      build_tags: ["example:version"],
      pull: {
        repository: "",
        tag: ""
      }
    };
  },
  computed: {
    build_text: {
      get: function() {
        return this.$refs["build-text"].text;
      },
      set: function(value) {
        this.$refs["build-text"].editText(value);
      }
    },
    build_args: {
      get: function() {
        return this.$refs["build-args"].text;
      },
      set: function(value) {
        this.$refs["build-args"].editText(value);
      }
    }
  },
  methods: {
    ...mapActions(["executeHost"]),
    goRefreshImageList: function() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.images",
          args: {
            all: false
          }
        }
      })
        .then(response => {
          this.image_list = response.data.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    goRefreshImageListWithFilters: function(filters) {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.images",
          args: {
            all: true,
            filters: filters
          }
        }
      })
        .then(response => {
          this.image_list = this.image_list.map(
            obj => response.data.data.find(o => o.Id === obj.Id) || obj
          );
        })
        .catch(error => {
          console.log(error);
        });
    },
    tryBuild: function() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.build",
          args: Object.assign({}, this.build_args, {
            fileobj: this.build_text
          })
        }
      })
        .then(response => {
          this.$refs["build-result"].addText(response.data);
          console.log(response);
        })
        .catch(error => {
          console.log(error);
        });
    },
    tryPull: function() {
      this.executeHost({
        id: this.host_id,
        data: {
          command: "api.pull",
          args: this.pull
        }
      })
        .then(response => {
          this.goRefreshImageList();
          console.log(response);
        })
        .catch(error => {
          console.log(error);
        });
    },
    tryReset: function() {
      this.build_text = "FROM image:version\nENTRYPOINT";
      this.build_args = 'tag: "example:version"\nnocache: false';
    }
  },
  mounted() {
    this.goRefreshImageList();
  }
};
</script>
