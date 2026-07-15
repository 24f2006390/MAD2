<script setup>
defineProps({
    status: String,
});
</script>

<template>
    <template v-if="status === 'pending'">
        <p class="badge bg-warning text-dark">Pending</p>
    </template>

    <template v-else-if="status === 'selected'">
        <p class="badge bg-success text-light">Selected</p>
    </template>

    <template v-else-if="status === 'rejected'">
        <p class="badge bg-danger text-light">Rejected</p>
    </template>

    <template v-else-if="status === 'shortlisted'">
        <p class="badge bg-info text-dark">Shortlisted</p>
    </template>

    <template v-else-if="status === 'approved'">
        <p class="badge bg-success">Approved</p>
    </template>

    <template v-else>
        <p class="badge text-dark">{{ status }}</p>
    </template>
</template>
