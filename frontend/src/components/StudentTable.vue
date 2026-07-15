<script setup>
import { storeToRefs } from "pinia";
import { CurrentUserStore } from "../stores/CurrentUser";
import StatusBadge from "./StatusBadge.vue";

defineProps({
    students: Array,
});

const userStore = CurrentUserStore();
const { role, user } = storeToRefs(userStore);

const backend_url = import.meta.env.VITE_API_URL;
</script>

<template>
    <div class="card border-0 shadow-sm rounded-4 mx-4 mt-5">
        <div class="table-responsive">
            <table class="table align-middle mb-0">
                <thead>
                    <tr class="text-uppercase text-muted small">
                        <th>Student</th>
                        <th>Branch</th>
                        <th>Degree</th>
                        <th>CGPA</th>
                        <th>Graduation</th>
                        <th v-if="role == 'admin'">Approval Status</th>

                        <th class="text-end">Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="student in students">
                        <!-- STUDENT INFO -->
                        <td>
                            <div class="d-flex align-items-center gap-3">
                                <img
                                    :src="
                                        student.photo_path
                                            ? `${backend_url}/${student.photo_path}`
                                            : `${backend_url}/static/images/Default_pfp.jpg`
                                    "
                                    class="rounded-circle"
                                    width="40"
                                    height="40"
                                />

                                <div>
                                    <div class="fw-semibold text-capitalize">
                                        {{ student.first_name }}
                                        {{ student.last_name }}
                                    </div>
                                    <small class="text-muted">
                                        {{ student.email_id }}
                                    </small>
                                </div>
                            </div>
                        </td>

                        <td class="text-uppercase">
                            {{ student.branch }}
                        </td>

                        <td class="text-uppercase">
                            {{ student.degree }}
                        </td>

                        <td>
                            <div class="d-flex align-items-center gap-2">
                                <span>{{ student.cgpa }}</span>

                                <div class="progress w-50" style="height: 6px">
                                    <div
                                        class="progress-bar"
                                        :style="`width:${student.cgpa * 10}%`"
                                    ></div>
                                </div>
                            </div>
                        </td>

                        <td>
                            {{ student.graduation_year }}
                        </td>

                        <td v-if="role == 'admin'">
                            <StatusBadge
                                :status="student.approval_status"
                            ></StatusBadge>
                        </td>

                        <td class="text-end">
                            <router-link
                                :to="`/student/${student.id}`"
                                class="text-decoration-none"
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
