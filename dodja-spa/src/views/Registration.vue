<template>
  <div>
    <b-form @submit="tryRegistration" @reset="onReset" v-if="!auth">
      <h1 class="text-center">{{ $t("registration") | capitalize }}</h1>
      <b-form-group
        label="Username:"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="username"
          v-model="input.username"
          placeholder="Enter Username"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        label="Email address:"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          v-model="input.email"
          type="email"
          placeholder="Enter Email"
        ></b-form-input>
      </b-form-group>

      <b-form-group label="Your Password:">
        <b-form-input
          v-model="input.password1"
          type="password"
          placeholder="Enter password"
          required
        ></b-form-input>
        <b-form-input
          v-model="input.password2"
          type="password"
          placeholder="Repeat password"
          required
          class="mt-2"
        ></b-form-input>
      </b-form-group>

      <b-button-group>
        <b-button type="submit" variant="primary">
          {{ $t("registration") | capitalize }}
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
  name: "Registration",
  data() {
    return {
      input: {
        username: "",
        password1: "",
        password2: "",
        email: ""
      }
    };
  },
  computed: {
    ...mapGetters(["auth"])
  },
  methods: {
    ...mapActions(["registration", "logout"]),
    ...mapMutations(["setMsg"]),
    tryRegistration(event) {
      // email !
      event.preventDefault();
      if (this.input.username == "" || this.input.password1 == "") {
        this.setMsg("Введите данные");
      } else if (this.input.password1 != this.input.password2) {
        this.setMsg("Повторите пароль");
      } else {
        this.registration({
          username: this.input.username,
          password1: this.input.password1,
          password2: this.input.password2
        })
          .then(response => {
            this.setMsg("Привет, " + response.data.user.username);
          })
          .catch(error => {
            this.setMsg("Введите данные: " + JSON.stringify(error.data.detail));
          });
      }
    },
    onReset(event) {
      event.preventDefault();
      this.input.username = "";
      this.input.password1 = "";
      this.input.password2 = "";
      this.input.email = "";
    },
    tryLogout() {
      this.logout().then(() => {
        this.setMsg("Выход");
      });
    }
  }
};
</script>
