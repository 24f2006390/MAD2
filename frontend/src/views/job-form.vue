<script setup>
import { useRouter, useRoute } from "vue-router";
import { api } from "../utils";
import { NotificationStore } from "../stores/NotificationStore";

const router = useRouter();
const route = useRoute();

const notificationStore = NotificationStore();
const company_id = route.params.id;

async function createJob(e) {
    const data = Object.fromEntries(new FormData(e.target).entries());

    try {
        const res = await api.post(`job/`, { ...data, company_id });
        notificationStore.add_message("success", "Job Created Successfully");

        router.push("/company/dashboard/");
    } catch (err) {
        console.log(err);
        notificationStore.add_message("danger", "Failed to create job");
    }
}
</script>

<template>
    <div class="container my-5">
        <div class="row justify-content-center">
            <div class="col-lg-7 col-md-9">
                <div class="card border-0 shadow-sm rounded-4">
                    <div class="card-body p-4 p-md-5">
                        <!-- Heading -->
                        <div class="text-center mb-4">
                            <i
                                class="bi bi-briefcase text-primary"
                                style="font-size: 48px"
                            ></i>

                            <h3 class="mt-2 fw-bold">Create A New Job</h3>
                        </div>

                        <!-- Form -->
                        <form @submit.prevent="createJob">
                            <!-- Job Title -->
                            <div class="mb-3">
                                <label class="form-label fw-semibold">
                                    Job Title
                                </label>

                                <div class="input-group input-group-lg">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-card-text"></i>
                                    </span>

                                    <input
                                        name="title"
                                        type="text"
                                        class="form-control rounded-end-3"
                                        placeholder="e.g. Software Engineer"
                                    />
                                </div>
                            </div>

                            <!-- Location -->
                            <div class="mb-3">
                                <label class="form-label fw-semibold">
                                    Location
                                </label>

                                <div class="input-group input-group-lg">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-geo-alt"></i>
                                    </span>

                                    <input
                                        name="location"
                                        type="text"
                                        class="form-control rounded-end-3"
                                        placeholder="e.g. Bangalore, India"
                                    />
                                </div>
                            </div>

                            <!-- Salary -->
                            <div class="mb-3">
                                <label class="form-label fw-semibold">
                                    Salary
                                </label>

                                <div class="input-group input-group-lg">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-currency-rupee"></i>
                                    </span>

                                    <input
                                        name="salary"
                                        type="text"
                                        class="form-control rounded-end-3"
                                        placeholder="e.g. 8–15 LPA"
                                    />
                                </div>
                            </div>

                            <!-- Experience -->
                            <div class="mb-3">
                                <label class="form-label fw-semibold">
                                    Experience
                                </label>

                                <div class="input-group input-group-lg">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-bar-chart-line"></i>
                                    </span>

                                    <input
                                        name="experience"
                                        type="text"
                                        class="form-control rounded-end-3"
                                        placeholder="e.g. 2–5 years"
                                    />
                                </div>
                            </div>

                            <!-- Description -->
                            <div class="mb-4">
                                <label class="form-label fw-semibold">
                                    Job Description
                                </label>

                                <div class="input-group">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-file-text"></i>
                                    </span>

                                    <textarea
                                        name="description"
                                        class="form-control rounded-end-3"
                                        rows="4"
                                        placeholder="Describe responsibilities, skills, requirements..."
                                    ></textarea>
                                </div>
                            </div>

                            <!-- Deadline -->
                            <div class="mb-4">
                                <label class="form-label fw-semibold">
                                    Application Deadline
                                </label>

                                <div class="input-group">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-calendar"></i>
                                    </span>

                                    <input
                                        name="application_deadline"
                                        type="date"
                                        class="form-control rounded-end-3"
                                    />
                                </div>
                            </div>

                            <!-- Submit -->
                            <button
                                type="submit"
                                class="btn btn-success container-fluid rounded-3"
                            >
                                <i class="bi bi-plus-circle me-2"></i>

                                Post Job
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
