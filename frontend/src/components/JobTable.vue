<script setup>
import StatusBadge from "./StatusBadge.vue";

const props = defineProps({
    jobs: {
        type: Array,
        default: () => [],
    },

    now: String,

    user: {
        type: String,
        default: "admin",
    },
});

function capitalize(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

function isDeadlinePassed(deadline) {
    return new Date(deadline) < new Date();
}
</script>

<template>
    <div class="card border-0 shadow-sm rounded-4 mx-4 mt-5">
        <div class="table-responsive">
            <table class="table align-middle mb-0">
                <!-- Table Head -->
                <thead>
                    <tr class="text-uppercase text-muted small">
                        <th>Job Title</th>

                        <th>Salary</th>
                        <th>Created Date</th>
                        <th>Application Deadline</th>
                        <th>Experience</th>

                        <template v-if="['admin', 'company'].includes(user)">
                            <th>Approval Status</th>
                        </template>

                        <th class="text-end">Actions</th>
                    </tr>
                </thead>

                <!-- Table Body -->
                <tbody>
                    <tr v-for="job in jobs" :key="job.id">
                        <!-- Job Title -->
                        <td>
                            <div class="fw-semibold">
                                {{ job.title }}
                            </div>

                            <small class="text-muted fw-semibold">
                                <i class="bi bi-geo-alt-fill text-danger"></i>

                                {{ job.location }}
                            </small>

                            <div
                                v-if="
                                    isDeadlinePassed(job.application_deadline)
                                "
                            >
                                <span class="badge bg-danger">
                                    Application Deadline is over
                                </span>
                            </div>
                        </td>

                        <!-- Salary -->
                        <td>
                            {{ job.salary }}
                        </td>

                        <!-- Created Date -->
                        <td class="text-muted">
                            {{ formatDate(job.created_at) }}
                        </td>

                        <!-- Deadline -->
                        <td class="text-muted">
                            {{ formatDate(job.application_deadline) }}
                        </td>

                        <!-- Experience -->
                        <td>
                            {{ job.experience }}
                        </td>

                        <!-- Admin / Company Columns -->
                        <template v-if="['admin', 'company'].includes(user)">
                            <!-- Approval Status -->
                            <td>
                                <StatusBadge :status="job.approval_status" />
                            </td>
                        </template>

                        <!-- Actions -->
                        <td class="text-end">
                            <div class="d-inline-flex gap-2">
                                <RouterLink
                                    :to="`/job/${job.id}`"
                                    class="btn btn-outline-success btn-sm"
                                >
                                    View Job
                                </RouterLink>
                            </div>
                        </td>
                    </tr>

                    <!-- Empty State -->
                    <tr v-if="jobs.length === 0">
                        <td colspan="8" class="text-center text-muted">
                            No Jobs Yet
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
