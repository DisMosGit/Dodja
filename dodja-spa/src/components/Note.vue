<template>
  <b-card class="text-center">
    <b-card-title
      ><b-form-input
        v-model="note.title"
        placeholder="Enter note title"
        :readonly="!edit_mode"
      ></b-form-input
    ></b-card-title>
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
      <b-button v-show="!edit_mode" variant="success" v-on:click="switchMe()">
        Edit
      </b-button>
      <b-button v-show="!edit_mode" variant="warning" v-on:click="refreshMe()">
        Refresh
      </b-button>
      <b-button v-show="edit_mode" variant="success" v-on:click="saveMe()">
        Save
      </b-button>
      <b-button v-show="edit_mode" variant="warning" v-on:click="switchMe()">
        Cancel
      </b-button>
      <b-button v-show="edit_mode" variant="danger" v-on:click="deleteMe()">
        Delete
      </b-button>
    </b-button-group>
  </b-card>
</template>

<script>
export default {
  name: "Note",
  props: ["note"],
  data() {
    return { edit_mode: false };
  },
  methods: {
    deleteMe: function() {
      this.$emit("remove", this.note.id);
    },
    saveMe: function() {
      this.$emit("save", this.note);
      this.switchMe();
    },
    refreshMe: function() {
      this.$emit("refresh", this.note.id);
    },
    switchMe: function() {
      this.edit_mode = !this.edit_mode;
    }
  }
};
</script>
