<script setup>
import { useRouter } from "vue-router";
import { api } from "../utils";
import { NotificationStore } from "../stores/NotificationStore";

const router = useRouter();
const notificationStore = NotificationStore();

async function createStudent(e) {
    const data = Object.fromEntries(new FormData(e.target).entries());

    try {
        await api.post(`student/`, data);
        console.log("registeration Successfull ");
        notificationStore.add_message("success", "Registeration Successful");

        router.push("/student/login/");
    } catch (err) {
        console.log(err);
        notificationStore.add_message("danger", "failed to register");
    }
}
</script>

<template>
    <div class="container my-5">
        <div class="row justify-content-center">
            <div class="col-lg-9 col-xl-8">
                <div class="card border-0 shadow-sm rounded-4">
                    <div class="card-body p-4 p-md-5">
                        <!-- Header -->
                        <div class="text-center mb-4">
                            <i class="bi bi-person-badge text-primary fs-1"></i>
                            <h3 class="fw-bold mt-2">Student Registration</h3>
                            <p class="text-muted mb-0">
                                Create your account to apply for placement
                                drives and jobs
                            </p>
                        </div>

                        <form @submit.prevent="createStudent">
                            <h6 class="fw-semibold mb-3 text-muted">
                                Personal & Academic Details
                            </h6>

                            <div class="row g-3">
                                <!-- First name -->
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >First Name</label
                                    >
                                    <div class="input-group input-group-lg">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-person"></i>
                                        </span>
                                        <input
                                            type="text"
                                            name="first_name"
                                            class="form-control"
                                            placeholder="First name"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- Last name -->
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Last Name</label
                                    >
                                    <div class="input-group input-group-lg">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-person"></i>
                                        </span>
                                        <input
                                            type="text"
                                            name="last_name"
                                            class="form-control"
                                            placeholder="Last name"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- Email -->
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Email</label
                                    >
                                    <div class="input-group input-group-lg">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-envelope"></i>
                                        </span>
                                        <input
                                            type="email"
                                            name="email_id"
                                            class="form-control"
                                            placeholder="example@email.com"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- Phone -->
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Phone Number</label
                                    >
                                    <div class="input-group input-group-lg">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-telephone"></i>
                                        </span>
                                        <input
                                            type="text"
                                            name="phone_no"
                                            class="form-control"
                                            placeholder="10-digit phone number"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- CGPA -->
                                <div class="col-md-4">
                                    <label class="form-label fw-semibold"
                                        >CGPA</label
                                    >
                                    <div class="input-group">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-bar-chart"></i>
                                        </span>
                                        <input
                                            type="number"
                                            step="0.01"
                                            name="cgpa"
                                            class="form-control"
                                            placeholder="8.5"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- Branch -->
                                <div class="col-md-4">
                                    <label class="form-label fw-semibold"
                                        >Branch</label
                                    >
                                    <div class="input-group">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-diagram-3"></i>
                                        </span>
                                        <input
                                            type="text"
                                            name="branch"
                                            class="form-control"
                                            placeholder="Computer Science"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- Graduation year -->
                                <div class="col-md-4">
                                    <label class="form-label fw-semibold"
                                        >Graduation Year</label
                                    >
                                    <div class="input-group">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-calendar"></i>
                                        </span>
                                        <input
                                            type="number"
                                            name="graduation_year"
                                            class="form-control"
                                            placeholder="2026"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- Degree -->
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Degree</label
                                    >
                                    <div class="input-group input-group-lg">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-mortarboard"></i>
                                        </span>
                                        <input
                                            type="text"
                                            name="degree"
                                            class="form-control"
                                            placeholder="B.Tech / M.Tech"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- Password -->
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Password</label
                                    >
                                    <div class="input-group input-group-lg">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-lock"></i>
                                        </span>
                                        <input
                                            type="password"
                                            name="password"
                                            class="form-control"
                                            placeholder="••••••••"
                                            required
                                        />
                                    </div>
                                </div>

                                <!-- Submit -->
                                <div class="col-12 d-grid mt-4">
                                    <button
                                        type="submit"
                                        class="btn btn-primary btn-lg"
                                    >
                                        <i class="bi bi-check-circle me-2"></i
                                        >Create Account
                                    </button>
                                </div>
                            </div>
                        </form>

                        <p class="text-center mt-4 mb-0">
                            Already registered?
                            <a href="/student/login" class="fw-semibold"
                                >Login</a
                            >
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
