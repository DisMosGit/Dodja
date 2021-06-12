import axios from "axios";

export default {
  state: {
    loadedNotes: [],
    ableNotes: []
  },
  getters: {
    loadedNotes: state => {
      return state.loadedNotes;
    },
    ableNotes: state => {
      return state.ableNotes;
    }
  },
  mutations: {
    saveNewNote: (state, payload) => {
      state.loadedNotes.push(payload);
    },
    editNoteByID: (state, payload) => {
      state.loadedNotes.every(function(hint, index) {
        if (hint.id == payload.id) {
          state.loadedNotes[index] = payload;
          return false;
        } else return true;
      });
    },
    forgetLatestNote: state => {
      state.loadedNotes.shift();
    },
    forgetNoteByKey: (state, key) => {
      state.loadedNotes.splice(
        state.loadedNotes.indexOf(x => x.key == key),
        1
      );
    },
    forgetAllNotes: state => {
      state.loadedNotes = [];
    },
    updateAbleNotes: (state, payload) => {
      payload.forEach(function(note_id) {
        if (state.loadedNotes.indexOf(note_id) === -1) {
          state.loadedHints.push(note_id);
        }
      });
    }
  },
  actions: {
    createNote: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post(`/api/host/${payload.host}/note/?format=json`, payload, {
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            console.log(error.response);
            reject(error.response);
          });
      });
    },
    getNoteList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/host/${payload.host}/note/?format=json`, {
            params: payload.params,
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            console.log(error);
            reject(error.response);
          });
      });
    },
    getNoteDetail: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/host/${payload.host}/note/${payload.id}/?format=json`, {
            params: payload.params,
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            reject(error.response);
          });
      });
    },
    updateNote: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .patch(
            `/api/host/${payload.host}/note/${payload.id}/?format=json`,
            payload,
            {
              headers: {
                Authorization: context.rootGetters.auth_header
              }
            }
          )
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            reject(error.response);
          });
      });
    },
    deleteNote: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .delete(`/api/host/${payload.host}/note/${payload.id}/?format=json`, {
            params: payload,
            headers: {
              Authorization: context.rootGetters.auth_header
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            reject(error.response);
          });
      });
    },
    loadNote: async (context, key) => {
      return new Promise((resolve, reject) => {
        if (!context.getters.loadedHints.find(x => x.key === key)) {
          context
            .dispatch("getNoteDetail", { key: key })
            .then(response => {
              context.commit("saveNewHint", response.data);
              resolve(true);
            })
            .catch(error => {
              this.setMsg("note error: " + JSON.stringify(error.data));
              reject(false);
            });
        }
      });
    },
    loadNotes: async (context, key) => {
      return new Promise((resolve, reject) => {
        if (!context.getters.loadedHints.find(x => x.key === key)) {
          context
            .dispatch("getNoteList", { key: key })
            .then(response => {
              context.commit("saveNewHint", response.data);
              resolve(true);
            })
            .catch(error => {
              this.setMsg("note error: " + JSON.stringify(error.data));
              reject(false);
            });
        }
      });
    }
  }
};
