<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { api } from "../utils";
import JobTable from "../components/JobTable.vue";
import { storeToRefs } from "pinia";
import { CurrentUserStore } from "../stores/CurrentUser";
import StatusBadge from "../components/StatusBadge.vue";
import { NotificationStore } from "../stores/NotificationStore";

const isEdit = ref(false);
let company = ref({});
const jobs = ref([]);

const route = useRoute();
const company_id = route.params.id;

const userStore = CurrentUserStore();
const notificationStore = NotificationStore();
const { role, user } = storeToRefs(userStore);

onMounted(async () => {
    try {
        let res = await api.get(`company/${company_id}/`);
        company.value = res.data;

        res = await api.get(`company/${company_id}/jobs`);
        jobs.value = res.data;
    } catch (err) {
        if (err.response) {
            const statusCode = err.response.status;
            if (statusCode == 403) {
                notificationStore.add_message(
                    "danger",
                    "Not Authorized to view this Company ",
                );
            }
        }
    }
});

async function updateCompany(e) {
    const data = Object.fromEntries(new FormData(e.target).entries());

    console.log(data);

    try {
        const res = await api.patch(`company/${company_id}/`, data);
        notificationStore.add_message(
            "success",
            "Updated Company Successfully",
        );

        company.value = res.data;
        isEdit.value = false;
    } catch (err) {
        console.log(err);
        notificationStore.add_message("danger", "Failed to update");
    }
}

async function approveCompany() {
    try {
        const res = await api.patch(`company/${company_id}/`, {
            approval_status: "approved",
        });
        company.value = res.data;
        notificationStore.add_message(
            "success",
            "Updated Company Successfully",
        );
    } catch (err) {
        console.log(err);
        notificationStore.add_message("danger", "Failed to update");
    }
}

async function rejectCompany() {
    try {
        const res = await api.patch(`company/${company_id}/`, {
            approval_status: "rejected",
        });
        company.value = res.data;
        notificationStore.add_message(
            "success",
            "Updated Company Successfully",
        );
    } catch (err) {
        console.log(err);
        notificationStore.add_message("danger", "Failed to update");
    }
}
</script>

<template>
    <form @submit.prevent="updateCompany">
        <div class="container py-4">
            <!-- HERO -->
            <div class="card border-0 shadow-sm rounded-4 mb-4">
                <div class="card-body p-4">
                    <div
                        class="d-flex justify-content-between align-items-start"
                    >
                        <!-- LEFT -->
                        <div class="d-flex gap-4">
                            <!-- LOGO -->
                            <div
                                class="bg-primary text-white rounded-3 d-flex align-items-center justify-content-center"
                                style="
                                    width: 110px;
                                    height: 110px;
                                    font-size: 40px;
                                "
                            >
                                {{ company.name && company.name[0] }}
                            </div>

                            <!-- INFO -->
                            <div>
                                <!-- NAME -->
                                <template v-if="isEdit">
                                    <input
                                        class="form-control mb-2"
                                        :value="company.name"
                                        name="name"
                                    />
                                </template>

                                <template v-else>
                                    <div
                                        class="d-flex align-items-center gap-2"
                                    >
                                        <h2 class="fw-bold mb-0">
                                            {{ company.name }}
                                        </h2>

                                        <StatusBadge
                                            :status="company.approval_status"
                                        ></StatusBadge>
                                    </div>
                                </template>

                                <!-- TAGLINE -->
                                <input
                                    name="tagline"
                                    v-if="isEdit"
                                    :value="company.tagline"
                                    class="form-control mb-2"
                                />

                                <p v-else class="text-muted">
                                    {{ company.tagline }}
                                </p>

                                <!-- META -->
                                <div class="small text-muted d-flex gap-3">
                                    <div>
                                        <i class="bi bi-building"></i>

                                        <template v-if="isEdit">
                                            <input
                                                name="industry"
                                                :value="company.industry"
                                                class="form-control d-inline w-auto ms-1"
                                            />
                                        </template>

                                        <template v-else>
                                            {{ company.industry }}
                                        </template>
                                    </div>

                                    <div>
                                        Founded:

                                        <template v-if="isEdit">
                                            <input
                                                name="founded_year"
                                                :value="company.founded_year"
                                                class="form-control d-inline w-auto ms-1"
                                            />
                                        </template>

                                        <template v-else>
                                            {{ company.founded_year }}
                                        </template>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- ACTIONS -->
                        <div v-if="role !== 'student'" class="d-flex gap-2">
                            <button
                                type="submit"
                                v-if="isEdit"
                                class="btn btn-primary"
                            >
                                Save
                            </button>

                            <button
                                v-if="isEdit"
                                @click="isEdit = false"
                                class="btn btn-light"
                            >
                                Cancel
                            </button>

                            <button
                                v-else
                                @click="isEdit = true"
                                class="btn btn-outline-primary"
                            >
                                Edit Company
                            </button>

                            <template v-if="isEdit == false && role == 'admin'">
                                <button
                                    class="btn btn-success"
                                    @click="approveCompany"
                                >
                                    Approve
                                </button>
                                <button
                                    class="btn btn-danger"
                                    @click="rejectCompany"
                                >
                                    Reject
                                </button>
                            </template>
                        </div>
                    </div>
                </div>
            </div>

            <!-- CONTENT -->
            <div class="row g-4">
                <!-- LEFT -->
                <div class="col-lg-8">
                    <!-- ABOUT -->
                    <div class="card border-0 shadow-sm rounded-4 mb-4">
                        <div class="card-body p-4">
                            <h5 class="fw-bold">About</h5>

                            <textarea
                                v-if="isEdit"
                                class="form-control"
                                rows="6"
                                :value="company.description"
                                name="description"
                            />

                            <p v-else class="text-muted">
                                {{ company.description }}
                            </p>
                        </div>
                    </div>

                    <!-- DETAILS -->
                    <div class="card border-0 shadow-sm rounded-4">
                        <div class="card-body p-4">
                            <h5 class="fw-bold mb-4">Company Details</h5>

                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="small text-muted">
                                        Staff Size
                                    </label>

                                    <input
                                        name="staff_size"
                                        v-if="isEdit"
                                        :value="company.staff_size"
                                        class="form-control"
                                    />

                                    <div v-else>
                                        {{ company.staff_size }}
                                    </div>
                                </div>

                                <div class="col-md-6">
                                    <label class="small text-muted">
                                        No. of Offices
                                    </label>

                                    <input
                                        name="no_of_offices"
                                        v-if="isEdit"
                                        :value="company.no_of_offices"
                                        class="form-control"
                                    />

                                    <div v-else>
                                        {{ company.no_of_offices }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- RIGHT -->
                <div class="col-lg-4">
                    <!-- CONTACT -->
                    <div class="card border-0 shadow-sm rounded-4 mb-4">
                        <div class="card-body p-4">
                            <h6 class="fw-bold mb-3">Contact</h6>

                            <div class="mb-3">
                                <i class="bi bi-envelope text-danger me-2"></i>
                                {{ company.hr_email }}
                            </div>

                            <div class="mb-3">
                                <i
                                    class="bi bi-telephone text-success me-2"
                                ></i>

                                <input
                                    name="hr_phone"
                                    v-if="isEdit"
                                    :value="company.hr_phone"
                                    class="form-control"
                                />

                                <span v-else>
                                    {{ company.hr_phone }}
                                </span>
                            </div>

                            <div>
                                <i class="bi bi-globe text-primary me-2"></i>

                                <input
                                    name="website"
                                    v-if="isEdit"
                                    :value="company.website"
                                    class="form-control"
                                />

                                <a
                                    v-else
                                    :href="company.website"
                                    target="_blank"
                                >
                                    {{ company.website }}
                                </a>
                            </div>
                        </div>
                    </div>

                    <!-- MAP -->
                    <div
                        class="card border-0 shadow-sm rounded-4 overflow-hidden"
                    >
                        <iframe
                            width="100%"
                            height="300"
                            style="border: 0"
                            loading="lazy"
                            :src="`https://www.google.com/maps?q=${company.hq_address}&output=embed`"
                        />

                        <div class="p-3 small">
                            <i class="bi bi-geo-alt text-primary"></i>

                            <div class="mt-2">
                                <textarea v-if="isEdit" class="form-control" />

                                <span v-else class="text-muted">
                                    {{ company.hq_address }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>

    <div class="row d-flex justify-content-center">
        <div class="col-10">
            <div class="card row d-flex justify-content-center m-5">
                <div class="card-body">
                    <JobTable :jobs="jobs" />
                </div>
            </div>
        </div>
    </div>
</template>
