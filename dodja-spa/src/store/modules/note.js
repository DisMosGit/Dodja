import axios from "axios";

export default {
  state: {
    loadedNotes: []
  },
  getters: {
    loadedNotes: state => {
      return state.loadedNotes;
    }
  },
  mutations: {
    saveNewNote: (state, payload) => {
      state.loadedNotes.push(payload);
    },
    saveNewNotes: (state, payload) => {
      payload.forEach(function(note) {
        state.loadedNotes.push(note);
      });
    },
    editNoteByID: (state, payload) => {
      state.loadedNotes.every(function(hint, index) {
        if (hint.id == payload.id) {
          state.loadedNotes[index] = payload;
          return false;
        } else return true;
      });
    },
    forgetNoteByID: (state, id) => {
      state.loadedNotes.splice(
        state.loadedNotes.indexOf(x => x.id == id),
        1
      );
    },
    forgetAllNotes: state => {
      state.loadedNotes = [];
    }
  },
  actions: {
    createNote: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .post(
            `/api/host/${payload.host_id}/note/?format=json`,
            payload.data,
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
            console.log(error.response);
            reject(error.response);
          });
      });
    },
    getNoteList: async (context, payload) => {
      return new Promise((resolve, reject) => {
        axios
          .get(`/api/host/${payload.host_id}/note/?format=json`, {
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
          .get(`/api/host/${payload.host_id}/note/${payload.id}/?format=json`, {
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
            `/api/host/${payload.host_id}/note/${payload.id}/?format=json`,
            payload.data,
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
          .delete(
            `/api/host/${payload.host_id}/note/${payload.id}/?format=json`,
            {
              params: payload.params,
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
    }
  }
};
