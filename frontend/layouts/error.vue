<template>
  <div class="error-page">
    <h1>Ошибка в маршруте!</h1>
    <p>Нажмите <a href="/">сюда</a>!</p>
  </div>
</template>


<script>

export default {
  
}

</script>


<style scoped>
.error-page {
  text-align: center;
}

.error-page a {
  text-decoration: none;
  color: tomato;
}

.error-page a:hover,
.error-page a:active {
  color: salmon;
}
</style>
