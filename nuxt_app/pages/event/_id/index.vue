<template>
  <div class="q-pa-md">
    <q-form @reset="onReset" class="q-gutter-md" @submit.prevent="onSubmit">
      <div class="q-pa-md beetween">
        <q-btn
          type="submit"
          color="primary"
          style="width:224px;"
        >{{!IsCreate ?"Редактировать" : "Добавить"}}</q-btn>
        <div style="max-width: 300px">
          <q-input filled v-model="event_date">
            <template v-slot:prepend>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale">
                  <q-date v-model="event_date" mask="YYYY-MM-DD HH:mm" />
                </q-popup-proxy>
              </q-icon>
            </template>

            <template v-slot:append>
              <q-icon name="access_time" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale">
                  <q-time v-model="event_date" mask="YYYY-MM-DD HH:mm" format24h />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>
        <q-btn
          label="сброс"
          type="reset"
          color="primary"
          flat
          class="q-ml-sm"
          style="width:224px;"
        />
        <q-btn v-show="!IsCreate" color="red" label="удалить" @click="delEvent" />
      </div>
      <div class="q-pa-md">
        <q-input
          filled
          v-model="title"
          label="заголовок *"
          lazy-rules
          :rules="[
          val => (val && val.length > 0) || 'введите заголовок',
        ]"
        ></q-input>
      </div>

      <div class="q-pa-md">
        <q-input
          v-model="description"
          filled
          type="textarea"
          label="описание *"
          :rules="[
          val => !!val || '* обязательное поле',
          val => val.length >= 3 || 'пароль не может быть меньше 3 символов'
        ]"
        />
      </div>
      <template>
        <div class="q-pa-md">
          <div class="q-gutter-md row items-start beetween">
            <q-date v-model="event_date" mask="YYYY-MM-DD HH:mm" color="purple" />
            <q-time v-model="event_date" mask="YYYY-MM-DD HH:mm" color="purple" />
          </div>
        </div>
      </template>
    </q-form>
  </div>
</template>


<script>
export default {
  middleware: "auth",
  computed: {},
  data() {
    return {
      IsCreate: undefined,
      id: "",
      title: "",
      description: "",
      event_date: ""
    };
  },
  mounted() {
    const { id } = this.$router.currentRoute.params;
    if (id !== "create" && !isNaN(id)) {
      let token,
        event,
        getEventsUrl = `/api/events/${id}`;
      token = localStorage.getItem("events_spa_token");
      this.$axios.setToken(`Token ${token}`);

      this.$axios
        .$get(getEventsUrl)
        .then(({ title, description, event_date }) => {
          this.IsCreate = false;
          this.id = id;
          this.title = title;
          this.description = description;
          this.event_date = this.$moment(event_date).format("YYYY-MM-DD HH:mm");
        })
        .catch(err => console.log("GET_EVENT_ERROR=>", err));
    } else if (id === "create") {
      this.IsCreate = true;
      this.event_date = this.$moment().format("YYYY-MM-DD HH:mm");
    }
  },

  methods: {
    onSubmit(e) {
      let token,
        event,
        url = !this.IsCreate ? `/api/events/${this.id}/` : "/api/events/",
        method = !this.IsCreate ? "put" : "post",
        message = !this.IsCreate
          ? `событие ${this.title} успешно отредактировано`
          : `событие ${this.title} успешно добавлено`;

      token = localStorage.getItem("events_spa_token");
      this.$axios.setToken(`Token ${token}`);
      event = {
        title: this.title,
        description: this.description,
        event_date: this.$moment(this.event_date).format()
      };

      this.$axios({
        method,
        url,
        data: event
      })
        .then(data => {
          this.$router.push("/");
          this.$q.notify({
            type: "success",
            message
          });
        })
        .catch(err => console.log(`${method}_EVENT_ERROR=>`, err));
    },
    onReset(e) {
      this.title = "";
      this.description = "";
      this.event_date = "";
    },
    delEvent(e) {
      if (this.id) {
        let token,
          deleteUrl = `/api/events/${this.id}/`,
          message = `событие ${this.title} успешно удалено`;

        token = localStorage.getItem("events_spa_token");
        this.$axios.setToken(`Token ${token}`);

        this.$axios
          .$delete(deleteUrl)
          .then(data => {
            this.$router.push("/");
            this.$q.notify({
              type: "success",
              message
            });
          })
          .catch(err => console.log(`$DELETE_EVENT_ERROR=>`, err));
      }
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
}
.beetween {
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
