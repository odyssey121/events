<template>
  <div class="header-container bg-grey-2">
    <header class="the-header">
      <TheSideNavToggle @toggle="$emit('sidenavToggle')" />
      <div class="logo">
        <nuxt-link to="/">Event$</nuxt-link>
      </div>
      <div class="navigation-items">
        <q-tabs v-show="getUser" active-color="orange" style="height:100%;">
          <q-route-tab to="/" label="События" exact />
          <q-route-tab to="event/create" label="Создать событие" exact />
        </q-tabs>

        <ul class="nav-list">
          <q-tabs v-show="getUser" active-color="orange" style="height:100%;"></q-tabs>
          <q-tabs v-show="!getUser" active-color="orange" style="height:100%;">
            <q-route-tab to="/auth" label="Авторизация" exact />
          </q-tabs>
          <q-tabs @click="logout" v-show="getUser" active-color="orange" style="height:100%;">
            <q-route-tab to label="Выход" exact />
          </q-tabs>
        </ul>
      </div>
    </header>
  </div>
</template>

<script>
import TheSideNavToggle from "~/components/Navigation/TheSideNavToggle";
export default {
  name: "TheHeader",
  components: { TheSideNavToggle },
  computed: {
    getUser() {
      return this.$store.getters["auth/getUser"];
    }
  },
  methods: {
    logout() {
      this.$store.dispatch("auth/unregister");
    }
  }
};
</script>
<style scoped>
.header-container {
  height: 54px;
  box-shadow: 0 1px 4px 0 rgba(0, 21, 41, 0.12);
  display: flex;
  justify-content: center;
  background: var(--sky);
}

.the-header {
  position: fixed;
  height: 54px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  z-index: 100;
  box-sizing: border-box;
  color: var(--text-grey);
}

.logo {
  width: 8rem;
  font-size: 1.3rem;
  margin-right: 1rem;
}

.logo a {
  text-decoration: none;
}

.navigation-items {
  display: none;
  height: 100%;
  width: 100%;
}

@media (min-width: 768px) {
  .navigation-items {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}
@media (max-width: 768px) {
  .the-header {
    left: 0;
  }
}

.nav-list {
  margin: auto 0;
  height: 85%;
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  font-size: 1rem;
  margin: 0 1.3rem;
  align-self: center;
}

.nav-item a {
  text-decoration: none;
}

.nav-item a:hover,
.nav-item a:active,
.nav-item a.nuxt-link-active {
  color: var(--active-color);
}
</style>
