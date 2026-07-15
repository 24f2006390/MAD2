<script setup>
import NotificationBar from "./components/NotificationBar.vue";
import NavBar from "./components/NavBar.vue";
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
    <NavBar v-if="route.path != '/'"></NavBar>

    <NotificationBar></NotificationBar>
    <router-view></router-view>
</template>
