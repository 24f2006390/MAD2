<script setup>
import { NotificationStore } from "../stores/NotificationStore.js";

const notificationStore = NotificationStore();
</script>
<template>
    <div>
        <p
            v-if="notificationStore.message"
            :class="`alert alert-${notificationStore.message_type}`"
        >
            {{ notificationStore.message }}
        </p>
    </div>
</template>
