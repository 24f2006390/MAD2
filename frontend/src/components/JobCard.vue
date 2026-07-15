<script setup>
import { CurrentUserStore } from "../stores/CurrentUser";

const UserStore = CurrentUserStore();

defineProps({
    job: Object,
});
</script>
<template>
    <div class="card border-0 shadow-sm rounded-4 h-100">
        <div class="card-body">
            <!-- Top badges -->
            <div class="d-flex justify-content-between mb-3">
                <span class="badge bg-light text-dark rounded-pill">
                    Full-time
                </span>

                <span class="badge bg-light text-dark rounded-pill">
                    3 days ago
                </span>
            </div>

            <!-- Main content -->
            <RouterLink
                :to="`/job/${job.id}`"
                class="text-decoration-none text-dark"
            >
                <h4 class="text-capitalize">
                    {{ job.title }}
                </h4>

                <p class="text-muted mb-1">
                    <i class="bi bi-buildings text-info"></i>
                    Google
                </p>

                <p class="text-muted mb-1">
                    <i class="bi bi-geo-alt text-danger"></i>
                    {{ job.location }}
                </p>

                <p class="text-muted">
                    <i class="bi bi-currency-dollar text-success"></i>
                    {{ job.salary }}
                </p>
            </RouterLink>
        </div>

        <div class="border-top mx-4"></div>

        <!-- Footer -->
        <div class="d-flex justify-content-between align-items-center p-3">
            <div></div>

            <RouterLink
                v-if="UserStore.role != 'student'"
                :to="`/job/${job.id}/applications/`"
                class="btn btn-outline-primary"
            >
                View Applicants
            </RouterLink>
        </div>
    </div>
</template>
