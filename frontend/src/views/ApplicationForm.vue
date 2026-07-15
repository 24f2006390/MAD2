<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "../utils";
import { CurrentUserStore } from "../stores/CurrentUser";
import { NotificationStore } from "../stores/NotificationStore";

const notificationStore = NotificationStore();

const userStore = CurrentUserStore();

const route = useRoute();
const router = useRouter();

const job_id = route.params.id;
const job = ref({});
const student = ref({});
const student_id = userStore.user.id;

onMounted(async () => {
    try {
        const [studentData, jobData] = await Promise.all([
            api.get(`student/${student_id}`),
            api.get(`job/${job_id}/`),
        ]);

        student.value = studentData.data;
        job.value = jobData.data;
    } catch (err) {
        console.log(err);
    }
});

async function createApplication(e) {
    const formData = new FormData(e.target);

    try {

        formData.append("student_id" , student_id)
        formData.append("job_id" , job_id)
        const res = await api.post(`application/`, formData );
        notificationStore.add_message(
            "success",
            "Application Created Successfully",
        );

        router.push(`/job/${job_id}/`);
    } catch (err) {
      console.log(err);
        const status_code = err.response?.status;
        if (status_code == 409) {
            notificationStore.add_message(
                "danger",
                "Multiple Applications are not allowed ",
            );
        } else {
            notificationStore.add_message(
                "danger",
                "Failed to create application",
            );
        }
    }
}
</script>
<template>
    <div class="container my-4">
        <div class="card border-0 shadow-sm rounded-4">
            <div class="card-body p-4">
                <div class="mb-4">
                    <h5 class="fw-bold mb-1">
                        Apply for
                        <router-link
                            :to="`/job/${job.id}/`"
                            class="text-decoration-none"
                        >
                            {{ job.title }}
                        </router-link>
                    </h5>
                    <p class="text-muted mb-0">Fill your details carefully</p>
                </div>

                <form
                    @submit.prevent="createApplication"
                    class="row g-3"
                    enctype="multipart/form-data"
                >
                    <!-- PROFILE PHOTO -->
                    <div class="col-12 text-center mb-2">
                        <div class="mb-2">
                            <!-- <img id="preview"
         src="/static/images/{{profile_path"
         class="rounded-circle border"
         style="width:110px;height:110px;object-fit:cover;"> -->
                        </div>
                    </div>

                    <input
                        name="job_id"
                        class="form-control"
                        :value="job.id"
                        hidden
                    />

                    <input
                        name="student_id"
                        class="form-control"
                        :value="student.id"
                        hidden
                    />

                    <!-- NAME -->
                    <div class="col-md-6">
                        <label class="form-label">First Name</label>
                        <input
                            name="first_name"
                            class="form-control"
                            :value="student.first_name"
                        />
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Last Name</label>
                        <input
                            name="last_name"
                            class="form-control"
                            :value="student.last_name"
                        />
                    </div>

                    <!-- CONTACT -->
                    <div class="col-md-6">
                        <label class="form-label">Email</label>
                        <input
                            name="email_id"
                            class="form-control"
                            :value="student.email_id"
                        />
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Phone</label>
                        <input
                            name="phone_no"
                            class="form-control"
                            :value="student.phone_no"
                        />
                    </div>

                    <!-- ACADEMIC -->
                    <div class="col-md-6">
                        <label class="form-label">Degree</label>
                        <input
                            name="degree"
                            class="form-control"
                            :value="student.degree"
                        />
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Branch</label>
                        <input
                            name="branch"
                            class="form-control"
                            :value="student.branch"
                        />
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">CGPA</label>
                        <input
                            name="cgpa"
                            class="form-control"
                            :value="student.cgpa"
                        />
                    </div>

                    <div class="col-md-6">
                        <label class="form-label">Graduation Year</label>
                        <input
                            name="graduation_year"
                            class="form-control"
                            :value="student.graduation_year"
                        />
                    </div>

                    <!-- RESUME -->
                    <div class="col-12">
                        <label class="form-label">Resume (PDF)</label>
                        <input name="resume" type="file" class="form-control" />
                    </div>

                    <!-- WHY HIRE -->
                    <div class="col-12">
                        <label class="form-label"
                            >Why should we hire you?</label
                        >

                        <textarea
                            name="why_hire"
                            class="form-control"
                            rows="4"
                        ></textarea>
                    </div>

                    <!-- ACTION -->
                    <div class="col-12 d-flex justify-content-end gap-2">
                        <button class="btn btn-outline-secondary">
                            Cancel
                        </button>

                        <button type="submit" class="btn btn-primary px-4">
                            Submit Application
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
