<script setup>
import StatusBadge from "./StatusBadge.vue";

defineProps({
    applications: Array,
});
function formatDate(date) {
    if (!date) return "";
    return new Date(date).toISOString().split("T")[0];
}

const backend_url =import.meta.env.VITE_API_URL;
</script>

<template>
    <div class="card border-0 shadow-sm rounded-4 mx-4 mt-5">
        <div class="table-responsive">
            <table class="table align-middle mb-0">
                <thead>
                    <tr class="text-uppercase text-muted small">
                        <th>Student Name</th>
                        <th>Applied at</th>
                        <th>Applied for</th>
                        <th>Applied Date</th>
                        <th>Score</th>
                        <th>Status</th>

                        <th class="text-end">Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <!-- Row 1 -->
                    <template v-for="application in applications">
                        <tr>
                            <td>
                                <div class="d-flex align-items-center gap-3">
                                    <img
                                        :src="
                                            application.student.photo_path
                                                ? `${backend_url}/${application.student.photo_path}`
                                                : `${backend_url}/static/images/Default_pfp.jpg`
                                        "
                                        class="rounded-circle"
                                        width="40"
                                        height="40"
                                    />
                                    <div>
                                        <div class="fw-semibold">
                                            {{
                                                application.student.first_name +
                                                " " +
                                                application.student.last_name
                                            }}
                                        </div>
                                        <small class="text-muted">{{
                                            application.student.email_id
                                        }}</small>
                                    </div>
                                </div>
                            </td>

                            <td class="text-uppercase">
                                {{ application.job.company.name }}
                            </td>
                            <td>{{ application.job.title }}</td>

                            <td class="text-muted">
                                {{ formatDate(application.created_at) }}
                            </td>

                            <td>
                                <strong>{{ application.student.cgpa }}</strong>
                                <small class="text-muted">/10</small>
                            </td>

                            <td>
                                <StatusBadge
                                    :status="application.status"
                                ></StatusBadge>
                            </td>

                            <td class="text-end">
                                <router-link
                                    :to="`/application/${application.id}`"
                                    class="btn btn-success"
                                    >View application</router-link
                                >
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
    </div>
</template>
