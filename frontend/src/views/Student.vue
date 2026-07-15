<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { api } from "../utils";
import { CurrentUserStore } from "../stores/CurrentUser";
import { NotificationStore } from "../stores/NotificationStore";
import StatusBadge from "../components/StatusBadge.vue";

const isEdit = ref(false);
const student = ref({});
const applications = ref([]);

const route = useRoute();
const userStore = CurrentUserStore();
const notificationStore = NotificationStore();

const student_id = route.params.id;

const backend_url = import.meta.env.VITE_API_URL;

// Fetch student data on load

async function fetch_data() {
    try {
        const [studentRes, appRes] = await Promise.all([
            api.get(`student/${student_id}`),
            api.get(`student/${student_id}/applications/`),
        ]);

        student.value = studentRes.data;
        applications.value = appRes.data;
    } catch (err) {
        console.error("Error fetching student:", err);
    }
}

onMounted(fetch_data);

async function updateStudent() {
    try {
        await api.patch(`student/${student_id}/`, student.value);
        isEdit.value = false;
        alert("Profile Updated!");
        notificationStore.add_message(
            "success",
            "Updated Student Successfully",
        );
    } catch (err) {
        console.error("Error updating student:", err);
        notificationStore.add_message("danger", "Failed to update");
    }
}

async function rejectStudent() {
    try {
        await api.patch(`student/${student_id}/`, {
            approval_status: "rejected",
        });
        isEdit.value = false;
        await fetch_data();
        alert("Profile Updated!");
    } catch (err) {
        console.error("Error updating student:", err);
    }
}

async function approveStudent() {
    try {
        await api.patch(`student/${student_id}/`, {
            approval_status: "approved",
        });
        isEdit.value = false;
        await fetch_data();
        alert("Profile Updated!");
    } catch (err) {
        console.error("Error updating student:", err);
    }
}

const selectedPhoto = ref(null);
const previewPhoto = ref(null);
function handlePhotoSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    selectedPhoto.value = file;
    previewPhoto.value = URL.createObjectURL(file);
}

async function uploadPhoto() {
    if (!selectedPhoto.value) return;

    const formData = new FormData();
    formData.append("photo", selectedPhoto.value);

    try {
        await api.patch(`student/${student_id}/`, formData);

        selectedPhoto.value = null;
        previewPhoto.value = null;

        await fetch_data();

        alert("Photo uploaded!");
    } catch (err) {
        console.error(err);
    }
}
</script>

<template>
    <div class="container my-4" v-if="student.id">
        <div class="card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-body">
                <div class="row align-items-center">
                    <!-- PHOTO -->
                    <div class="col-md-3 text-center">
                        <img
                            :src="
                                previewPhoto ||
                                (student.photo_path
                                    ? `${backend_url}/${student.photo_path}`
                                    : `${backend_url}/static/images/Default_pfp.jpg`)
                            "
                            class="rounded-circle border"
                            style="
                                width: 130px;
                                height: 130px;
                                object-fit: cover;
                            "
                        />

                        <div v-if="isEdit" class="mt-3">
                            <input
                                type="file"
                                accept="image/*"
                                class="form-control form-control-sm mb-2"
                                @change="handlePhotoSelect"
                            />

                            <button
                                class="btn btn-sm btn-primary w-100"
                                @click="uploadPhoto"
                                :disabled="!selectedPhoto"
                            >
                                Upload Photo
                            </button>
                        </div>

                        <h5 class="mt-2 text-capitalize">
                            {{ student.first_name }} {{ student.last_name }}
                        </h5>

                        <small class="text-muted">
                            {{ student.email_id }}
                            <span class="badge bg-light text-dark">
                                <status-badge
                                    :status="student.approval_status"
                                />
                            </span>
                        </small>
                    </div>

                    <!-- STATS -->
                    <div class="col-md-9">
                        <div class="d-flex justify-content-between mb-3">
                            <h5 class="fw-bold">Career Overview</h5>

                            <!-- Buttons  -->
                            <div class="d-flex gap-2">
                                <template v-if="userStore.role == 'admin'">
                                    <button
                                        v-if="!isEdit"
                                        type="button"
                                        class="btn btn-success"
                                        @click="approveStudent"
                                    >
                                        Approve
                                    </button>
                                    <button
                                        v-if="!isEdit"
                                        type="button"
                                        class="btn btn-danger"
                                        @click="rejectStudent"
                                    >
                                        Reject
                                    </button>
                                </template>

                                <template v-if="isEdit">
                                    <button
                                        class="btn btn-success"
                                        @click="updateStudent"
                                    >
                                        Save Profile
                                    </button>
                                    <button
                                        class="btn btn-secondary"
                                        type="button"
                                        @click="isEdit = false"
                                    >
                                        Cancel
                                    </button>
                                </template>
                                <button
                                    v-else
                                    type="button"
                                    @click="isEdit = true"
                                    class="btn btn-primary"
                                >
                                    Edit Profile
                                </button>
                            </div>
                        </div>

                        <div class="row g-3">
                            <div class="col-md-4">
                                <div class="border rounded p-3 text-center">
                                    <div class="text-muted small">
                                        Applied Jobs
                                    </div>
                                    <h4>{{ applications?.length || 0 }}</h4>
                                </div>
                            </div>

                            <div class="col-md-4">
                                <div class="border rounded p-3 text-center">
                                    <div class="text-muted small">
                                        Shortlisted
                                    </div>
                                    <h4>
                                        {{
                                            applications.filter(
                                                (item) =>
                                                    item.status.toLowerCase() ==
                                                    "shortlisted",
                                            ).length
                                        }}
                                    </h4>
                                </div>
                            </div>

                            <div class="col-md-4">
                                <div class="border rounded p-3 text-center">
                                    <div class="text-muted small">Selected</div>
                                    <h4 class="text-success">
                                        {{
                                            applications.filter(
                                                (item) =>
                                                    item.status.toLowerCase() ==
                                                    "selected",
                                            ).length
                                        }}
                                    </h4>
                                </div>
                            </div>
                        </div>

                        <!-- CGPA BAR -->
                        <div class="mt-3">
                            <div class="d-flex justify-content-between">
                                <div v-if="isEdit" class="mb-2 w-100">
                                    <label class="form-label small"
                                        >Edit CGPA</label
                                    >
                                    <input
                                        type="number"
                                        step="0.01"
                                        min="0"
                                        max="10"
                                        class="form-control form-control-sm"
                                        v-model="student.cgpa"
                                    />
                                </div>
                                <template v-else>
                                    <small>CGPA</small>
                                    <small class="fw-bold"
                                        >{{ student.cgpa }}/10</small
                                    >
                                </template>
                            </div>

                            <div class="progress" style="height: 8px">
                                <div
                                    class="progress-bar"
                                    :style="{ width: student.cgpa * 10 + '%' }"
                                ></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- PROFILE FORM -->
        <div class="card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label fw-bold">First Name</label>
                        <input
                            class="form-control"
                            v-model="student.first_name"
                            :disabled="!isEdit"
                        />
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-bold">Last Name</label>
                        <input
                            class="form-control"
                            v-model="student.last_name"
                            :disabled="!isEdit"
                        />
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-bold">Phone</label>
                        <input
                            class="form-control"
                            v-model="student.phone_no"
                            :disabled="!isEdit"
                        />
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-bold">Branch</label>
                        <input
                            class="form-control"
                            v-model="student.branch"
                            :disabled="!isEdit"
                        />
                    </div>
                </div>
            </div>
        </div>

        <!-- APPLICATIONS TABLE -->
        <div class="card border-0 shadow-sm rounded-4">
            <div class="card-body">
                <h5 class="fw-bold mb-3">Applications</h5>
                <table class="table align-middle">
                    <thead class="small text-muted">
                        <tr>
                            <th>Job</th>
                            <th>Company</th>
                            <th>Status</th>
                            <th class="text-end">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="app in applications" :key="app.id">
                            <td>{{ app.job.title }}</td>
                            <td>{{ app.job.company.name }}</td>
                            <td>
                                <StatusBadge :status="app.status"></StatusBadge>
                            </td>

                            <td class="text-end">
                                <router-link
                                    :to="`/application/${app.id}`"
                                    class="btn btn-sm btn-outline-primary"
                                    >View</router-link
                                >
                            </td>
                        </tr>
                        <tr v-if="applications.length == 0">
                            <td colspan="4" class="text-center text-muted">
                                No applications yet
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
