<script setup>
defineProps({
    icon_name: String,
    stat_num: Number,
    title: String,
});
</script>

<template>
    <div class="card h-100 shadow-sm p-4">
        <div class="d-flex justify-content-between">
            <div class="icon-box text-primary fs-3">
                <i :class="icon_name"></i>
            </div>
        </div>

        <h1 class="fw-bold mt-4 mb-1">{{ stat_num }}</h1>
        <p class="text-muted mb-0">{{ title }}</p>
    </div>
</template>
