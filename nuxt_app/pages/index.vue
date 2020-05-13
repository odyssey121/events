<template></template>

<script>
export default {
  components: {},
  middleware: "auth",
  created() {
    this.$store.dispatch("auth/getUser");
  }
};
</script>

<style>
</style>
