<template>
  <b-sidebar id="sidebar-right" sidebar-class="border" right shadow lazy>
    <template #header="{ hide }">
      <b-button block variant="outline-danger" size="sm" @click="hide">
        {{ $t("close") | capitalize }}
      </b-button>
    </template>
    <div id="sidebar-right-content" class="p-2">
      <b-button
        block
        variant="outline-primary"
        size="sm"
        class="mb-1"
        @click="addEmptyNote"
      >
        {{ $tc("add") | capitalize }}
      </b-button>
      <Note
        v-for="note in notes"
        v-bind:key="note.id"
        v-bind:note="note"
      ></Note>
    </div>
  </b-sidebar>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import Note from "@/components/Note";

export default {
  name: "SidebarRight",
  components: {
    Note
  },
  data() {
    return { notes: [] };
  },
  computed: {
    ...mapGetters(["loadedNotes"]),
    host_id: function() {
      return this.$route.params.id;
    }
  },
  methods: {
    ...mapActions(["getNoteList"]),
    addEmptyNote: function() {
      this.notes.push({
        id: "new",
        host: this.host_id,
        text: "",
        date_updated: new Date()
      });
    }
  },
  watch: {
    host_id: function() {
      if (this.host_id) {
        this.getNoteList({ host: this.host_id })
          .then(response => {
            this.notes = response.data;
          })
          .catch(error => {
            console.log(error.response);
          });
      } else {
        this.notes = [];
      }
    }
  },
  mounted() {
    if (this.host_id) {
      this.getNoteList({ host: this.host_id })
        .then(response => {
          this.notes = response.data;
        })
        .catch(error => {
          console.log(error.response);
        });
    }
  }
};
</script>
