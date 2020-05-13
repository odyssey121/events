<template>
  <div id="main-layout">
    <TheHeader @sidenavToggle="toggleView" />
    <TheSideNav @close="toggleView" :show="showToggle"></TheSideNav>
    <div class="container">
      <nuxt />
    </div>
  </div>
</template>

<script>
import TheHeader from "~/components/Navigation/TheHeader";
import TheSideNav from "~/components/Navigation/TheSideNav";
import { mapGetters, mapActions } from "vuex";

export default {
  components: { TheHeader, TheSideNav },
  mounted() {
    const token = localStorage.getItem('events_spa_token');
    if(token){
      this.$store.dispatch('auth/getUser');
    }
    this.$store.subscribe((mutation, state) => {
      switch (mutation.type) {
        case "auth/SET_USER":
          if (state.auth.user !== null) {
            this.$router.push("/");
            this.$q.notify({
              message: `вы авторизировались с именем пользователя: ${state.auth.user.username}`
            });
          }
      }
    });
  },

  created() {
    this.$q.loadingBar.setDefaults({
      color: "orange",
      size: "2px",
      position: "top"
    });
  },

  data() {
    return {
      showToggle: false
    };
  },
  methods: {
    toggleView() {
      this.showToggle = !this.showToggle;
    }
  }
};
</script>

<style scoped>
</style>
