<script setup>
import { ref, computed, onMounted } from "vue";
import { api } from "../utils";
import { CurrentUserStore } from "../stores/CurrentUser";

//  Components
import StatCard from "../components/StatCard.vue";
import JobCard from "../components/JobCard.vue";
import { useRouter } from "vue-router";
import { NotificationStore } from "../stores/NotificationStore";

const router = useRouter();
const notificationStore = NotificationStore();

const userStore = CurrentUserStore();

console.log("In the dashboard");
console.log("Role value", userStore.role);
console.log("usr value", userStore.user);

const company = ref({});
const jobs = ref([]);
const applications_ct = ref(0);
const selected_applications_ct = ref(0);

const company_id = userStore.user.id;

console.log(company_id);
onMounted(async () => {
    try {
        const  res = await api.get(`company_dash_data/${company_id}/`);
        const data = res.data ;
        company.value = data["company"];
        jobs.value = data["company_jobs"];
        applications_ct.value = data["total_app_ct"];
        selected_applications_ct.value = data["selected_app_ct"];
    } catch (err) {
        console.log(err);
        userStore.logout()
        notificationStore.add_message("danger", "Not Logged In");
        router.push("/admin/login/");
    }
});

const stats = computed(() => [
    {
        title: "Total Jobs Posted",
        icon_name: "bi-briefcase",
        stat_num: jobs.value.length,
    },
    {
        title: "Total Applicants",
        icon_name: "bi-people",
        stat_num: applications_ct.value,
    },
    {
        title: "Selected Students",
        icon_name: "bi-check-circle",
        stat_num: selected_applications_ct.value,
    },
]);
</script>

<template>
    <!--  Company Info  -->
    <div class="card">
        <div class="card-body d-flex align-items-center gap-5">
            <!--  Company logo -->

            <div
                class="text-white bg-primary d-flex align-items-center justify-content-center rounded-3"
                style="width: 100px; height: 100px; font-size: 40px"
            >
                G
            </div>

            <!--  Company detail -->
            <div>
                <h3 class="fw-bold mb-3">{{ company.name }}</h3>

                <div class="text-muted">
                    <p class="mb-2">
                        <i class="bi bi-envelope me-1"></i>
                        {{ company.hr_email }}
                    </p>

                    <p class="mb-2">
                        <i class="bi bi-geo-alt me-1 text-danger"></i>
                        {{ company.hq_address }}
                    </p>

                    <p class="mb-2">
                        <i class="bi bi-telephone me-1 text-success"></i>
                        {{ company.hr_phone }}
                    </p>

                    <p class="mb-0">
                        <i class="bi bi-globe me-1 text-primary"></i>
                        <a target="_blank" rel="noopener noreferrer">
                            {{ company.website }}
                        </a>
                    </p>
                </div>

                <button class="btn btn-outline-primary mt-2">
                    <RouterLink
                        :to="`/company/${company.id}/`"
                        class="text-decoration-none"
                    >
                        View Company Details
                    </RouterLink>
                </button>
            </div>
        </div>
    </div>

    <div class="my-5 px-4 mb-3">
        <h2 class="fw-bold mb-1">Dashboard Overview</h2>
        <p class="text-muted mb-1">
            Welcome back, here's what's happening today.
        </p>
    </div>

    <!-- stats -->
    <div class="row gap-4 mx-2">
        <StatCard
            v-for="stat in stats"
            :title="stat.title"
            :icon_name="stat.icon_name"
            :stat_num="stat.stat_num"
            class="p-4 col"
        ></StatCard>
    </div>

    <!-- Jobs section -->
    <div class="mt-5 p-4 d-flex align-items-center justify-content-between">
        <div>
            <h3>Recently Added Job Roles</h3>
            <small class="text-muted fs-5">
                Manage Individual roles and view applicants for this
                drive.</small
            >
        </div>

        <div>
            <router-link
                :to="`/company/${company.id}/jobs/?status=all`"
                class="fw-bold text-decoration-none px-4"
            >
                <i class="bi bi-plus"></i> View all
            </router-link>

            <router-link :to="`/company/${company.id}/job-form/`">
                <button class="btn btn-primary px-4">
                    <i class="bi bi-plus"></i> Add new Job
                </button>
            </router-link>
        </div>
    </div>

    <!-- jobs card  -->
    <div class="row row-cols-3 g-2">
        <JobCard class="col" v-for="job in jobs" :job="job"></JobCard>

        <!-- Job placeholder  card -->
        <div class="col">
            <div class="card rounded-4 shadow-sm border border-dashed h-100">
                <div
                    class="card-body d-flex flex-column justify-content-center align-items-center text-center py-5"
                >
                    <RouterLink
                        :to="`/company/${company.id}/job-form/`"
                        class="rounded-circle bg-light d-flex align-items-center justify-content-center text-decoration-none mb-3"
                        style="width: 64px; height: 64px"
                    >
                        <i class="bi bi-plus-lg fs-3 text-secondary"></i>
                    </RouterLink>

                    <h6 class="fw-semibold mb-1">Add Another Job</h6>

                    <small class="text-muted">
                        Expand the recruitment scope
                    </small>
                </div>
            </div>
        </div>
    </div>
</template>
