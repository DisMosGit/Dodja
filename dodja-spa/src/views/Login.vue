<template>
  <div>
    <b-form @submit="tryLogin" @reset="onReset" v-if="!auth">
      <h1 class="text-center">{{ $t("login") | capitalize }}</h1>
      <b-form-group label="Your Username:">
        <b-form-input
          v-model="input.username"
          type="text"
          placeholder="Enter Username"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Your Password:">
        <b-form-input
          v-model="input.password"
          type="password"
          placeholder="Enter Password"
          required
        ></b-form-input>
      </b-form-group>

      <b-button-group>
        <b-button type="submit" variant="primary">
          {{ $t("login") | capitalize }}
        </b-button>
        <b-button type="reset" variant="warning">
          {{ $t("reset") | capitalize }}
        </b-button>
      </b-button-group>
    </b-form>
    <div v-else>
      <h1 class="text-center">{{ $t("logout") | capitalize }}</h1>
      <b-button variant="outline-danger" block @click="tryLogout">
        {{ $t("logout") | capitalize }}
      </b-button>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";

export default {
  name: "Login",
  data() {
    return {
      input: {
        username: "",
        password: ""
      }
    };
  },
  computed: {
    ...mapGetters(["auth"])
  },
  methods: {
    ...mapActions(["login", "logout"]),
    ...mapMutations(["setMsg"]),
    tryLogin(event) {
      event.preventDefault();
      if (this.input.username != "" && this.input.password != "") {
        this.login(this.input)
          .then(response => {
            this.setMsg("Привет: " + response.data.user.username);
          })
          .catch(error => {
            this.setMsg("Пользователь не существует: " + error.data);
          });
      } else {
        this.setMsg("Введите логин и пароль");
      }
    },
    onReset(event) {
      event.preventDefault();
      this.input.username = "";
      this.input.password = "";
    },
    tryLogout() {
      this.logout().then(() => {
        this.setMsg("Выход");
      });
    }
  }
};
</script>
