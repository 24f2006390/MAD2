<script setup>
import StatusBadge from "./StatusBadge.vue";

defineProps({
    companies: Array,
});
</script>

<template>
    <div class="card border-0 shadow-sm rounded-4 mx-4 mt-5">
        <div class="table-responsive">
            <table class="table align-middle mb-0">
                <thead>
                    <tr class="text-uppercase text-muted small">
                        <th>Company</th>
                        <th>Industry</th>
                        <th>Location</th>
                        <th>Employees</th>

                        <th>Status</th>
                        <th class="text-end">Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="company in companies">
                        <!-- COMPANY INFO -->
                        <td>
                            <div class="d-flex align-items-center gap-3">
                                <div class="bg-light rounded p-2">
                                    <i class="bi bi-buildings text-primary"></i>
                                </div>

                                <div>
                                    <div class="fw-semibold text-capitalize">
                                        {{ company.name }}
                                    </div>

                                    <small class="text-muted">
                                        Since {{ company.founded_year }}
                                    </small>
                                </div>
                            </div>
                        </td>

                        <td>{{ company.industry }}</td>

                        <td>
                            <i class="bi bi-geo-alt"></i>
                            {{ company.hq_address }}
                        </td>

                        <td>
                            {{ company.staff_size }}
                        </td>

                        <td>
                            <!-- {{ status(company.approval_status) }} -->
                            <StatusBadge
                                :status="company.approval_status"
                            ></StatusBadge>
                        </td>

                        <td class="text-end">
                            <router-link
                                :to="`/company/${company.id}`"
                                class="btn btn-sm btn-primary"
                            >
                                View
                            </router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
