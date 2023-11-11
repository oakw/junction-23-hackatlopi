<script setup>
import SideBar from "./components/SideBar.vue";
import Chat from "./components/Chat.vue";
import Analysis from "./components/Analysis.vue";
import Performance from "./components/Performance.vue";
</script>

<template>
  <div class="grid grid-cols-8 w-full py-12 px-10 h-full auto-rows-fr">
    <SideBar />

    <Chat />

    <Analysis />

    <Performance />
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
