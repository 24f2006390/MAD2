<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { api } from "../utils";
import { CurrentUserStore } from "../stores/CurrentUser";
import ApplicationTable from "../components/ApplicationTable.vue";
import StatusBadge from "../components/StatusBadge.vue";
import { NotificationStore } from "../stores/NotificationStore";

const userStore = CurrentUserStore();
const notificationStore = NotificationStore();
const role = ref(userStore.role);

const route = useRoute();
const job_id = route.params.id;

const job = ref({});
const company = ref({});
const applications = ref([]);

const isEdit = ref(false);

const now = new Date();

onMounted(async () => {
    try {
        const jobData = await api.get(`job/${job_id}/`);

        job.value = jobData.data;

        const companyData = await api.get(`company/${job.value.company_id}/`);

        company.value = companyData.data;

        if (userStore.role != "student") {
            const res = await api.get(`job/${job_id}/applications/`);
            applications.value = res.data;
        }
    } catch (err) {
        if (err.response) {
            const statusCode = err.response.status;

            if (statusCode == "403") {
                notificationStore.add_message(
                    "danger",
                    "not Authorized to view this job",
                );
            }
        }
    }
});

const isDeadlinePassed = computed(() => {
    if (!job.value) return false;

    return new Date(job.value.application_deadline) < now;
});

const mapUrl = computed(() => {
    if (!job.value?.location) return "";

    return `https://www.google.com/maps?q=${encodeURIComponent(job.value.location)}&output=embed`;
});

async function updateJob(e) {
    try {
        const data = Object.fromEntries(new FormData(e.target).entries());
        const res = await api.patch(`job/${job_id}/`, data);
        job.value = res.data;
        isEdit.value = false;

        notificationStore.add_message("success", "Updated Job Successfully");
    } catch (err) {
        console.log(err);
        notificationStore.add_message("danger", "Failed to update ");
    }
}

async function closeJob() {
    try {
        const res = await api.patch(`job/${job_id}/`, { is_closed: true });
        job.value = res.data;
    } catch (err) {
        console.log(err);
    }
}

async function approveJob() {
    try {
        const res = await api.patch(`job/${job_id}/`, {
            approval_status: "approved",
        });

        job.value = res.data;
    } catch (err) {
        console.log(err);
    }
}

async function rejectJob() {
    try {
        const res = await api.patch(`job/${job_id}/`, {
            approval_status: "rejected",
        });

        job.value = res.data;
    } catch (err) {
        console.log(err);
    }
}

function formatDate(date) {
    if (!date) return "";
    return new Date(date).toISOString().split("T")[0];
}
</script>

<template>
    <form @submit.prevent="updateJob">
        <div v-if="job">
            <!-- HEADER -->
            <div class="bg-white border-bottom">
                <div class="container py-4">
                    <div
                        class="d-flex justify-content-between align-items-start"
                    >
                        <!-- LEFT -->
                        <div class="d-flex gap-3">
                            <div
                                class="bg-dark text-white rounded-3 d-flex align-items-center justify-content-center"
                                style="width: 56px; height: 56px"
                            >
                                <span class="fw-semibold"> T </span>
                            </div>

                            <div>
                                <small class="text-primary fw-semibold">
                                    JOB OPENING
                                </small>

                                <small class="text-muted ms-2">
                                    Full-time
                                </small>

                                <span
                                    v-if="isDeadlinePassed"
                                    class="badge bg-danger ms-2"
                                >
                                    Application Deadline is over
                                </span>

                                <StatusBadge
                                    :status="job.approval_status"
                                ></StatusBadge>

                                <div v-if="isEdit">
                                    <input
                                        name="title"
                                        :value="job.title"
                                        class="form-control mb-2"
                                    />
                                </div>

                                <h3 v-else class="fw-bold mb-1 text-capitalize">
                                    {{ job.title }}
                                </h3>

                                <div
                                    class="d-flex flex-wrap gap-3 text-muted small text-capitalize"
                                >
                                    <span>
                                        <i class="bi bi-building"></i>
                                        {{ company.name }}
                                    </span>

                                    <span>
                                        <i class="bi bi-geo-alt me-1"></i>

                                        <input
                                            v-if="isEdit"
                                            name="location"
                                            :value="job.location"
                                            class="form-control d-inline w-auto"
                                        />

                                        <template v-else>
                                            {{ job.location }}
                                        </template>
                                    </span>

                                    <span>
                                        <i class="bi bi-cash me-1"></i>

                                        <input
                                            v-if="isEdit"
                                            name="salary"
                                            :value="job.salary"
                                            class="form-control d-inline w-auto"
                                        />

                                        <template v-else>
                                            {{ job.salary }}
                                        </template>
                                    </span>

                                    <span>
                                        <i class="bi bi-briefcase me-1"></i>

                                        <input
                                            v-if="isEdit"
                                            name="experience"
                                            :value="job.experience"
                                            class="form-control d-inline w-auto"
                                        />

                                        <template v-else>
                                            {{ job.experience }}
                                        </template>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- ACTIONS -->

                        <div
                            v-if="role === 'company' || role === 'admin'"
                            class="m-2 d-flex gap-2"
                        >
                            <template v-if="!isEdit">
                                <button
                                    class="btn btn-primary"
                                    @click="isEdit = true"
                                >
                                    Edit
                                </button>

                                <button
                                    v-if="
                                        role === 'admin' &&
                                        job.approval_status !== 'approved'
                                    "
                                    class="btn btn-success"
                                    @click="approveJob"
                                >
                                    Approve
                                </button>

                                <button
                                    v-if="
                                        role === 'admin' &&
                                        job.approval_status !== 'rejected'
                                    "
                                    class="btn btn-danger"
                                    @click="rejectJob"
                                >
                                    Reject
                                </button>
                            </template>

                            <template v-else>
                                <button type="submit" class="btn btn-primary">
                                    Save Changes
                                </button>

                                <button
                                    class="btn btn-danger"
                                    @click="isEdit = false"
                                >
                                    Cancel
                                </button>
                            </template>
                        </div>
                        <div v-else>
                            <router-link
                                :to="`/job/${job.id}/application-form/`"
                                class="btn btn-success"
                            >
                                Apply now</router-link
                            >
                        </div>
                    </div>
                </div>
            </div>

            <!-- MAIN -->
            <div class="bg-light">
                <div class="container py-4">
                    <div class="row g-4">
                        <!-- LEFT -->
                        <div class="col-lg-8">
                            <!-- DESCRIPTION -->
                            <div class="card border-0 shadow-sm rounded-4 mb-4">
                                <div class="card-body p-4">
                                    <h5 class="fw-bold mb-3">
                                        Job Description
                                    </h5>

                                    <textarea
                                        v-if="isEdit"
                                        name="description"
                                        v-model="job.description"
                                        rows="8"
                                        class="form-control"
                                    ></textarea>

                                    <div
                                        v-else
                                        class="text-muted"
                                        v-html="job.description"
                                    ></div>
                                </div>
                            </div>

                            <!-- DETAILS -->
                            <div class="card border-0 shadow-sm rounded-4">
                                <div class="card-body p-4">
                                    <h5 class="fw-bold mb-3">Job Details</h5>

                                    <ul class="list-unstyled d-grid gap-3 mb-0">
                                        <li class="d-flex gap-3">
                                            <i
                                                class="bi bi-calendar-event-fill text-primary"
                                            ></i>

                                            Application Deadline:

                                            <input
                                                v-if="isEdit"
                                                type="date"
                                                name="application_deadline"
                                                :value="
                                                    formatDate(
                                                        job.application_deadline,
                                                    )
                                                "
                                                class="form-control w-auto"
                                            />

                                            <strong v-else>
                                                {{
                                                    formatDate(
                                                        job.application_deadline,
                                                    )
                                                }}
                                            </strong>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <!-- RIGHT -->
                        <div class="col-lg-4">
                            <!-- COMPANY -->
                            <div class="card border-0 shadow-sm rounded-4 mb-4">
                                <div class="card-body p-4">
                                    <h6 class="fw-bold mb-2">
                                        Company Overview
                                    </h6>

                                    <p class="text-muted small">
                                        {{ company.description }}
                                    </p>

                                    <div class="small">
                                        <div
                                            class="d-flex justify-content-between"
                                        >
                                            <span class="text-muted">
                                                Website
                                            </span>

                                            <a
                                                :href="company.website"
                                                class="fw-semibold text-decoration-none"
                                            >
                                                {{ company.website }}
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- MAP -->
                            <div class="card border-0 shadow-sm rounded-4">
                                <div class="card-body p-0">
                                    <iframe
                                        width="100%"
                                        height="300"
                                        style="border: 0"
                                        loading="lazy"
                                        class="img-fluid rounded-top"
                                        :src="mapUrl"
                                    ></iframe>

                                    <div class="p-3 small">
                                        <i
                                            class="bi bi-geo-alt text-primary"
                                        ></i>

                                        Job Location

                                        <br />

                                        <span class="text-muted">
                                            {{ job.location }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>

    <div
        v-if="userStore.role != 'student'"
        class="card container border-0 shadow-sm rounded-4 mb-4"
    >
        <div class="card-body">
            <div class="d-flex justify-content-between">
                <h5 class="fw-bold mb-3">Received Applications for the Job</h5>

                <router-link
                    :to="`/job/${job.id}/applications/`"
                    class="text-decoration-none"
                >
                    + View All</router-link
                >
            </div>

            <ApplicationTable :applications="applications"></ApplicationTable>
        </div>
    </div>
</template>
