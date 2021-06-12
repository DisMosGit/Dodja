<template>
  <b-card :title="note.id" class="text-center">
    <b-card-sub-title class="mb-2">
      {{ note.date_updated | toDate }}
    </b-card-sub-title>
    <b-card-text class="text-justify text-wrap text-break">
      <b-form-textarea
        v-model="note.text"
        placeholder="Enter your text"
        no-auto-shrink
        :disabled="!edit_mode"
      ></b-form-textarea>
    </b-card-text>
    <b-button-group size="sm">
      <b-button v-if="!edit_mode" variant="success" v-on:click="switchMe()">
        Edit
      </b-button>
      <b-button v-if="!edit_mode" variant="warning" v-on:click="refreshMe()">
        Refresh
      </b-button>
      <b-button v-if="edit_mode" variant="success" v-on:click="saveMe()">
        Save
      </b-button>
      <b-button v-if="edit_mode" variant="warning" v-on:click="switchMe()">
        Cancel
      </b-button>
      <b-button v-if="edit_mode" variant="danger" v-on:click="deleteMe()">
        Delete
      </b-button>
    </b-button-group>
  </b-card>
</template>

<script>
import { mapMutations, mapActions } from "vuex";

export default {
  name: "Note",
  props: ["note"],
  data() {
    return { edit_mode: false };
  },
  methods: {
    ...mapMutations(["deleteHintByKey"]),
    ...mapActions([""]),
    deleteMe: function() {
      console.log("deleteMe");
      // this.deleteHintByKey(this.hint.key);
    },
    saveMe: function() {
      console.log("saveMe");
      // this.deleteHintByKey(this.hint.key);
    },
    refreshMe: function() {
      console.log("refreshMe");
    },
    switchMe: function() {
      this.edit_mode = !this.edit_mode;
    }
  }
};
</script>
