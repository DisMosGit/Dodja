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
        v-for="note in loadedNotes"
        v-bind:key="note.id"
        v-bind:note="note"
        v-on:save="saveNote"
        v-on:remove="removeNote"
        v-on:refresh="refreshNote"
      ></Note>
    </div>
  </b-sidebar>
</template>

<script>
import { mapGetters, mapActions, mapMutations, mapState } from "vuex";
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
    ...mapState([
      {
        n: "loadedNotes"
      }
    ]),
    ...mapGetters(["loadedNotes"]),
    host_id: function() {
      return this.$route.params.id;
    }
  },
  methods: {
    ...mapMutations([
      "saveNewNote",
      "saveNewNotes",
      "editNoteByID",
      "forgetNoteByID",
      "forgetAllNotes"
    ]),
    ...mapActions([
      "getNoteDetail",
      "getNoteList",
      "deleteNote",
      "createNote",
      "updateNote"
    ]),
    addEmptyNote: function() {
      this.saveNewNote({
        id: "new",
        title: "",
        host: this.host_id,
        text: "",
        date_updated: new Date()
      });
    },
    saveNote: function(data) {
      if (data.id != "new") {
        this.updateNote({
          host_id: this.host_id,
          id: data.id,
          data: data
        }).then(response => {
          this.editNoteByID(response.data);
        });
      } else {
        this.createNote({ host_id: this.host_id, data: data }).then(
          response => {
            this.forgetNoteByID(data.id);
            this.saveNewNote(response.data);
          }
        );
      }
    },
    removeNote: function(id) {
      this.forgetNoteByID(id);
      if (id != "new") {
        this.deleteNote({ host_id: this.host_id, id: id }).then(() => {});
      }
    },
    refreshNotes: function() {
      this.forgetAllNotes();
      this.getNoteList({ host_id: this.host_id }).then(response => {
        this.saveNewNotes(response.data);
      });
    },
    refreshNote: function(id) {
      this.getNoteDetail({ host_id: this.host_id, id: id }).then(response => {
        this.editNoteByID(response.data);
      });
    }
  },
  watch: {
    host_id: function(nV) {
      if (nV) {
        this.refreshNotes();
      } else {
        this.forgetAllNotes();
      }
    }
  },
  mounted() {
    if (this.host_id && !this.notes) {
      this.refreshNotes();
    }
  }
};
</script>
