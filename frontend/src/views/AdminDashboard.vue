<script setup>
import { onMounted, ref } from "vue";
import StatCard from "../components/StatCard.vue";
import StudentTable from "../components/StudentTable.vue";
import { api } from "../utils";
import StatusBadge from "../components/StatusBadge.vue";

const jobs = ref([]);
const companies = ref([]);
const students = ref([]);
const applications = ref([]);

onMounted(async () => {
    let res = await api.get("admin_dash_data/");
    const data = res.data;

    jobs.value = data["jobs"];
    companies.value = data["companies"];
    students.value = data["students"];
    applications.value = data["applications"];
});
</script>

<template>
    <!-- Dashboard stats  -->

    <div
        class="d-flex justify-content-between align-items-center mt-5 px-4 mb-3"
    >
        <div>
            <h2 class="fw-bold mb-1">Dashboard Overview</h2>
            <p class="text-muted mb-0">
                Welcome back, here's what's happening today.
            </p>
        </div>
    </div>

    <div class="m-5">
        <div class="row gap-3">
            <StatCard
                :stat_num="jobs.length"
                title="Total Jobs Posted"
                icon_name="bi-briefcase"
                class="col"
            ></StatCard>

            <StatCard
                :stat_num="companies.length"
                title="Total Companies Registered"
                icon_name="bi-building"
                class="col"
            ></StatCard>

            <StatCard
                :stat_num="students.length"
                title="Total Students Registered"
                icon_name="bi-person"
                class="col"
            >
            </StatCard>

            <StatCard
                :stat_num="applications.length"
                title="Total Applications Made"
                icon_name="bi-file-text"
                class="col"
            ></StatCard>
        </div>
    </div>
    <div class="row g-5 px-4 mx-auto mt-3">
        <div class="container py-4">
            <!-- ROW 1 -->
            <div class="row g-4">
                <!-- RECENT JOB POSTINGS -->
                <div class="col-lg-6">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-body">
                            <div class="d-flex justify-content-between mb-3">
                                <h5 class="fw-bold">Recent Job Postings</h5>
                                <router-link
                                    to="/jobs/"
                                    class="text-decoration-none"
                                >
                                    View All</router-link
                                >
                            </div>

                            <table class="table align-middle">
                                <thead class="small text-muted">
                                    <tr>
                                        <th>JOB TITLE</th>
                                        <th>COMPANY</th>
                                        <th>PACKAGE</th>
                                        <th class="text-end">ACTION</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    <template v-for="job in jobs">
                                        <tr>
                                            <td>
                                                <div class="fw-semibold">
                                                    {{ job.title }}
                                                </div>
                                                <small class="text-muted"
                                                    >Full Time</small
                                                >
                                            </td>

                                            <td>{{ job.company.name }}</td>

                                            <td
                                                class="text-success fw-semibold"
                                            >
                                                {{ job.salary }}
                                            </td>

                                            <td class="text-end">
                                                <router-link
                                                    class="btn btn-sm btn-outline-primary"
                                                    :to="`/job/${job.id}/`"
                                                >
                                                    View Details
                                                </router-link>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- NEW REGISTRATIONS -->
                <div class="col-lg-6">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-body">
                            <div class="d-flex justify-content-between mb-3">
                                <h5 class="fw-bold">New Registrations</h5>
                                <router-link
                                    to="/companies/"
                                    class="text-decoration-none"
                                    >View All</router-link
                                >
                            </div>

                            <table class="table align-middle">
                                <thead class="small text-muted">
                                    <tr>
                                        <th>COMPANY NAME</th>
                                        <th>INDUSTRY</th>
                                        <th>STATUS</th>
                                        <th class="text-end">ACTION</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    <template v-for="company in companies">
                                        <tr>
                                            <td>
                                                <div
                                                    class="d-flex align-items-center gap-2"
                                                >
                                                    <div
                                                        class="bg-light rounded p-2"
                                                    >
                                                        {{ company.name[0] }}
                                                    </div>
                                                    {{ company.name }}
                                                </div>
                                            </td>

                                            <td>{{ company.industry }}</td>

                                            <td>
                                                <StatusBadge
                                                    :status="
                                                        company.approval_status
                                                    "
                                                >
                                                </StatusBadge>
                                            </td>

                                            <td class="text-end">
                                                <router-link
                                                    :to="`/company/${company.id}`"
                                                    class="btn btn-sm btn-primary"
                                                >
                                                    Review
                                                </router-link>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ROW 2 - STUDENTS -->
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex justify-content-between mb-3">
                                <h5 class="fw-bold">Latest Student Sign-ups</h5>

                                <router-link
                                    to="/students/"
                                    class="text-decoration-none"
                                >
                                    View All Students
                                </router-link>
                            </div>

                            <!-- {{ student_table(students[: 5]) }} -->
                            <StudentTable :students="students"></StudentTable>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
