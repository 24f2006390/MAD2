<script setup>
import NotificationBar from "./components/NotificationBar.vue";
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>

    <NotificationBar></NotificationBar>
    <router-view></router-view>
</template>
