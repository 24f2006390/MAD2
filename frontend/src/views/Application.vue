<script setup>
import { onMounted, ref } from "vue";
import { api } from "../utils";
import { useRoute } from "vue-router";
import { CurrentUserStore } from "../stores/CurrentUser";
import { storeToRefs } from "pinia";
import { NotificationStore } from "../stores/NotificationStore";

const userStore = CurrentUserStore();
const notificationStore = NotificationStore();

const { role, user } = storeToRefs(userStore);

const route = useRoute();
const app_id = route.params.id;

const application = ref({});

const remark = ref("test");
const status = ref("all");

const backend_url = import.meta.env.VITE_API_URL;

onMounted(async () => {
    try {
        const res = await api.get(`application/${app_id}/`);
        application.value = res.data;
        console.log(application.value)
        status.value = application.value.status;
        remark.value = application.value.remark;
    } catch (err) {
        console.log(err);
    }
});




function openresume(resume_path){

  console.log(resume_path)
  const url = `${backend_url}/${resume_path}/`
  console.log(url)
  window.open(url, '_blank')

}


function updateApplication() {
    try {
        const res = api.patch(`application/${app_id}/`, {
            remark: remark.value,
            status: status.value,
        });
        console.log("Updated application");
        notificationStore.add_message(
            "success",
            "Updated Application Successfully",
        );
    } catch (err) {
        console.log(err);
        notificationStore.add_message("danger", "Failed To update Application");
    }
}
</script>

<template>
    <div class="container my-4">
        <div class="card border-0 shadow-sm rounded-4">
            <div class="card-body p-4">
                <!-- HEADER -->
                <div class="d-flex justify-content-between mb-3">
                    <div>
                        <h5 class="fw-bold mb-1">Application Details</h5>
                        <p class="text-muted mb-0 fw-bold">
                            Applied for:
                            <router-link
                                :to="`/job/${application.job_id}/`"
                                class="text-decoration-none"
                            >
                                <i class="bi bi-briefcase text-primary"></i>
                                {{ application.job?.title }}
                            </router-link>
                        </p>
                    </div>
                </div>

                <div class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label">Name</label>
                        <div class="form-control bg-light">
                            {{ application.student?.first_name }}
                            {{ application.student?.last_name }}
                        </div>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Email</label>
                        <div class="form-control bg-light">
                            {{ application.student?.email_id }}
                        </div>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Phone</label>
                        <div class="form-control bg-light">
                            {{ application.student?.phone_no }}
                        </div>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Degree</label>
                        <div class="form-control bg-light">
                            {{ application.student?.degree }}
                        </div>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Branch</label>
                        <div class="form-control bg-light">
                            {{ application.student?.branch }}
                        </div>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">CGPA</label>
                        <div class="form-control bg-light">
                            {{ application.student?.cgpa }}
                        </div>
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Graduation Year</label>
                        <div class="form-control bg-light">
                            {{ application.student?.graduation_year }}
                        </div>
                    </div>

                    <!-- APPLICATION.STUDENT SUBMITTED DATA -->

                    <div class="col-12">
                        <label class="form-label"
                            >Why should we Hire you ?</label
                        >
                        <div
                            class="form-control bg-light"
                            style="min-height: 120px"
                        >
                            {{ application.why_hire || "None" }}
                        </div>
                    </div>

                    <div class="col-12">
                        <button
                                type="button"
                                class="btn btn-outline-primary"
                                :disabled="!application.resume_path"
                                @click="openresume(application.resume_path)"
                            >
                                View Resume
                        </button>
                    </div>
                </div>

                <hr />

                <!-- INTERVIEWER ACTION FORM -->

                <div class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label">Decision</label>

                        <select
                            name="status"
                            class="form-select"
                            v-model="status"
                            :disabled="role == 'student'"
                        >
                            <option value="pending">Pending</option>
                            <option value="shortlisted">Shortlisted</option>

                            <option value="selected">Selected</option>

                            <option value="rejected">Rejected</option>
                        </select>
                    </div>

                    <div class="col-12">
                        <label class="form-label">Interviewer Remark</label>

                        <textarea
                            name="remark"
                            class="form-control"
                            rows="4"
                            v-model="remark"
                            :disabled="role == 'student'"
                        ></textarea>
                    </div>

                    <div
                        v-if="role != 'student'"
                        class="col-12 d-flex justify-content-end gap-2"
                    >
                        <router-link
                            :to="`/student/${application.student?.id}/`"
                            class="btn btn-outline-primary"
                        >
                            View Student
                        </router-link>

                        <button
                            @click="updateApplication"
                            class="btn btn-primary px-4"
                        >
                            Update Decision
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
