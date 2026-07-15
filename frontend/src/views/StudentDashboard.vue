<script setup>
import { ref, onMounted } from "vue";
import { api } from "../utils";

import { CurrentUserStore } from "../stores/CurrentUser";
import StatCard from "../components/StatCard.vue";
import JobCard from "../components/JobCard.vue";
import { NotificationStore } from "../stores/NotificationStore";

const userStore = CurrentUserStore();
const notificationStore = NotificationStore();

const student = ref({});
const companies = ref([]);
const jobs = ref([]);
const total_app_ct = ref(0);
const selected_app_ct = ref(0);

const student_id = userStore.user.id;

console.log(student_id);
onMounted(async () => {
    try {
        // const res  = await api.get(`student_dash_data/${student_id}/`)
        const res = await api.get(`student_dash_data/${student_id}/`);
        const data = res.data;
        student.value = data["student"];
        jobs.value = data["jobs"];
        companies.value = data["companies"];
        total_app_ct.value = data["total_app_ct"];
        selected_app_ct.value = data["selected_app_ct"];
    } catch (err) {
        console.error(err);
    }
});


async function export_student_history(){

  try {

    const res = await api.get(`/student/${student_id}/export/`) ;
    notificationStore.add_message("success","Your CSV file has been successfully sent to your email")

  }
  catch(err){
    notificationStore.add_message("danger", "Unknown Error occured")
  }
}


</script>

<template>
    <h3 class="display-5 mt-5 ms-5">Welcome Back , {{ student.first_name }}</h3>

    <div class="mt-5 p-4 d-flex align-items-center justify-content-between">
        <div>
            <h3>Dashboard Overview</h3>
            <small class="text-muted fs-5">
                Welcome back, here's what's happening today.</small
            >
        </div>

        <div>

            <button @click="export_student_history()" class="btn btn-primary" > Export history </button>

        </div>
    </div>

    <div class="d-flex gap-2 mx-2 mx-5">
        <StatCard
            class="col-lg-4 col-md-6"
            title="Total Jobs to apply"
            :stat_num="jobs.length"
            icon_name="bi-briefcase"
        ></StatCard>

        <StatCard
            class="col-lg-4 col-md-6"
            title="Total Applications made "
            :stat_num="total_app_ct"
            icon_name="bi bi-people"
        ></StatCard>

        <StatCard
            class="col-lg-4 col-md-6"
            title="Selected for jobs"
            :stat_num="selected_app_ct"
            icon_name="bi bi-people"
        ></StatCard>
    </div>

    <div class="mt-5 p-4 d-flex align-items-center justify-content-between">
        <div>
            <h3>Top companies hiring</h3>
            <small class="text-muted fs-5">
                Top recruiters are actively hiring</small
            >
        </div>
    </div>

    <div class="row g-3 m-4">
        <template v-for="company in companies">
            <div class="col-lg-4 col-md-6">
                <div class="card h-100 shadow-sm">
                    <!-- HEADER -->
                    <div class="card-body">
                        <div class="d-flex align-items-center mb-2">
                            <div class="bg-light rounded p-2 me-3">
                                <i
                                    class="bi bi-buildings text-primary fs-4"
                                ></i>
                            </div>

                            <div>
                                <h5 class="mb-0 text-capitalize">
                                    {{ company.name }}
                                </h5>

                                <small class="text-muted">
                                    <i class="bi bi-geo-alt"></i>
                                    {{ company.hq_address }}
                                </small>
                            </div>
                        </div>

                        <!-- INFO BADGES -->
                        <div class="mb-2">
                            <span class="badge bg-light text-dark border">
                                {{ company.industry }}
                            </span>

                            <span class="badge bg-light text-dark border">
                                {{ company.staff_size }} employees
                            </span>
                        </div>

                        <!-- DESCRIPTION -->
                        <p class="small text-muted">
                            {{ company.description }}
                        </p>

                        <!-- STATS -->
                        <div class="d-flex justify-content-between small mb-3">
                            <div>
                                <i class="bi bi-briefcase text-primary"></i>
                                {{ company.jobs | length }} Jobs
                            </div>

                            <div>
                                <i class="bi bi-calendar"></i>
                                Since {{ company.founded_year }}
                            </div>
                        </div>

                        <!-- ACTIONS -->
                        <div class="d-grid gap-2">
                            <router-link
                                :to="`/company/${company.id}/`"
                                class="btn btn-primary btn-sm"
                            >
                                View Details
                            </router-link>

                            <router-link
                                :to="`/company/${company.id}/jobs`"
                                class="btn btn-outline-secondary btn-sm"
                            >
                                Open Jobs
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </div>

    <!--  Jobs  -->

    <div class="mt-5 p-4 d-flex align-items-center justify-content-between">
        <div>
            <h3>Recently Added Job Roles</h3>
            <small class="text-muted fs-5">
                Manage Individual roles and view applicants for this
                drive.</small
            >
        </div>
        <div>
            <a
                href="/jobs/?status=all"
                class="fw-bold text-decoration-none px-4"
            >
                <i class="bi bi-plus"></i> View all
            </a>
        </div>
    </div>

    <div class="row row-cols-3 g-2 mx-2">
        <JobCard v-for="job in jobs" :job="job"></JobCard>
        <!-- {% from "component/job_card.html" import job_card %}
  {% set jobs =  jobs | selectattr('is_closed' ,'equalto' , 0) | list  %}
  {% for job in jobs %}
     {{job_card(job  ,now=now , student_id = student.id) }}
  {% endfor %} -->
    </div>
</template>
