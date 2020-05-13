<template>
  <div class="q-pa-md login-form">
    <div>
      <q-btn-toggle
        v-model="isLogin"
        toggle-color="primary"
        push
        glossy
        :options="[
          { label: 'Логин', value: true },
          { label: 'Регистрация', value: false }
        ]"
      />
    </div>
    <q-form @reset="onReset" class="q-gutter-md">
      <q-input
        filled
        v-model="email"
        label="ваш email *"
        hint="ваш email адресс"
        lazy-rules
        :rules="[
          val => (val && val.length > 0) || 'введите email адресс',
          val => /\S+@\S+\.\S+/.test(val) || 'неверный email адресс'
        ]"
      >
        <template v-slot:append>
          <q-icon name="email" />
        </template>
      </q-input>

      <q-input
        v-model="password1"
        filled
        :type="isPwd ? 'password' : 'text'"
        hint="пароль"
        label="введите пароль *"
        :rules="[
          val => !!val || '* обязательное поле',
          val => val.length >= 3 || 'пароль не может быть меньше 3 символов'
        ]"
      >
        <template v-slot:append>
          <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
          />
        </template>
      </q-input>

      <q-input
        v-show="!isLogin"
        v-model="password2"
        filled
        :type="isPwd ? 'password' : 'text'"
        hint="повтор пароля"
        label="повторите пароль *"
        :rules="[
          val => !!val || '* обязательное поле',
          val => val.length >= 3 || 'пароль2 не может быть меньше 3 символов'
        ]"
      >
        <template v-slot:append>
          <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
          />
        </template>
      </q-input>

      <div class="q-pa-md btn-bottom">
        <q-btn type="submit" color="primary" style="width:224px;" @click="onSubmit">
          {{
          isLogin ? "Логин" : "Регистрация"
          }}
        </q-btn>
        <q-btn label="сброс" type="reset" color="primary" flat class="q-ml-sm" />
      </div>
    </q-form>
  </div>
</template>

<script>
export default {
  computed: {},
  data() {
    return {
      isPwd: true,
      isLogin: true,
      email: "",
      password1: "",
      password2: ""
    };
  },
  methods: {
    onSubmit(e) {
      this.$store
        .dispatch("auth/authenticateUser", {
          isLogin: this.isLogin,
          email: this.email,
          password1: this.password1,
          password2: this.password2
        })
        .then(() => this.$store.dispatch("auth/getUser"))
        .catch(err => {
          const { response } = err;
          if (response) {
            if (response.request.responseURL.endsWith("/login/")) {
              this.$q.notify({
                type: "warning",
                message: "авторизация не пройдена, неверный логин или пароль"
              });
            } else {
              for (let [key, value] of Object.entries(response.data)) {
                let message;
                this.$q.notify({
                  type: "warning",
                  message: `${JSON.stringify(value)
                    .split(/[\{\[]/)
                    .join("")
                    .split(/[\}\]]/)
                    .join("")}`
                });
              }
            }
          } else {
            console.log("NOT REQUES RESPONSE ERROR =>", err);
          }
        });
    },
    onReset() {
      this.email = "";
      this.password1 = "";
      this.password2 = "";
    }
  }
};
</script>

<style scoped>
.auth-container {
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 2px #ccc;
  width: 300px;
  margin: auto;
  padding: 10px;
  box-sizing: border-box;
}
.login-form {
  margin: auto;
  margin-top: 10%;
  max-width: 400px;
}
.btn-bottom {
  display: flex;
  justify-content: space-between;
}
.login-form > div {
  width: 100;
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}
</style>
