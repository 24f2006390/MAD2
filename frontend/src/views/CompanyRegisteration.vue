<script setup>
import { useRouter, useRoute } from "vue-router";
import { api } from "../utils";
import { NotificationStore } from "../stores/NotificationStore";

const router = useRouter();

const notificationStore = NotificationStore();

async function createCompany(e) {
    const data = Object.fromEntries(new FormData(e.target).entries());
    try {
        await api.post(`company/`, { ...data });

        console.log("Registeration Successfull");
        notificationStore.add_message(
            "success",
            "Company Registered Successfully",
        );

        router.push("/company/login/");
    } catch (err) {
        console.log(err);
        notificationStore.add_message("danger", "Failed To register");
    }
}
</script>

<template>
    <div class="container my-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card border-0 shadow-sm rounded-4">
                    <div class="card-body p-4 p-md-5">
                        <!-- Header -->
                        <div class="text-center mb-4">
                            <i class="bi bi-building text-primary fs-1"></i>
                            <h3 class="fw-bold mt-2">Company Registration</h3>
                            <p class="text-muted mb-0">
                                Access your placement dashboard
                            </p>
                        </div>

                        <form @submit.prevent="createCompany">
                            <!-- Company Name -->
                            <div class="mb-3">
                                <label class="form-label fw-semibold"
                                    >Company Name</label
                                >
                                <div class="input-group input-group-lg">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-building"></i>
                                    </span>
                                    <input
                                        type="text"
                                        name="name"
                                        class="form-control"
                                        placeholder="e.g. Google"
                                        required
                                    />
                                </div>
                            </div>

                            <!-- Website + HR Email -->
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Company Website</label
                                    >
                                    <div class="input-group input-group-lg">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-globe"></i>
                                        </span>
                                        <input
                                            type="url"
                                            name="website"
                                            class="form-control"
                                            placeholder="https://google.com"
                                            required
                                        />
                                    </div>
                                </div>

                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >HR Email</label
                                    >
                                    <div class="input-group input-group-lg">
                                        <span class="input-group-text bg-white">
                                            <i class="bi bi-envelope"></i>
                                        </span>

                                        <input
                                            type="email"
                                            name="hr_email"
                                            class="form-control"
                                            placeholder="hr@company.com"
                                            required
                                        />
                                    </div>
                                </div>
                            </div>

                            <!-- HR Phone -->
                            <div class="mb-3 mt-3">
                                <label class="form-label fw-semibold"
                                    >HR Phone</label
                                >
                                <div class="input-group input-group-lg">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-telephone"></i>
                                    </span>
                                    <input
                                        type="tel"
                                        name="hr_phone"
                                        class="form-control"
                                        placeholder="+91 98765 43210"
                                        required
                                    />
                                </div>
                            </div>

                            <!-- HQ Address -->
                            <div class="mb-3">
                                <label class="form-label fw-semibold"
                                    >HQ Address</label
                                >
                                <div class="input-group">
                                    <span class="input-group-text bg-white">
                                        <i class="bi bi-geo-alt"></i>
                                    </span>
                                    <textarea
                                        name="hq_address"
                                        rows="3"
                                        class="form-control"
                                        placeholder="Company headquarters address"
                                        required
                                    ></textarea>
                                </div>
                            </div>

                            <!-- Tagline + Industry -->
                            <div class="row g-3 mb-3">
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Tagline</label
                                    >
                                    <input
                                        type="text"
                                        name="tagline"
                                        class="form-control"
                                        placeholder="Innovating the future"
                                        required
                                    />
                                </div>

                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Industry</label
                                    >
                                    <input
                                        type="text"
                                        name="industry"
                                        class="form-control"
                                        placeholder="Software / Finance / Manufacturing"
                                        required
                                    />
                                </div>
                            </div>

                            <!-- Founded Year -->
                            <div class="mb-3">
                                <label class="form-label fw-semibold"
                                    >Founded Year</label
                                >
                                <input
                                    type="number"
                                    name="founded_year"
                                    class="form-control"
                                    min="1800"
                                    max="2099"
                                    placeholder="e.g. 2005"
                                    required
                                />
                            </div>

                            <!-- Description -->
                            <div class="mb-3">
                                <label class="form-label fw-semibold"
                                    >Company Description</label
                                >
                                <textarea
                                    name="description"
                                    rows="4"
                                    class="form-control"
                                    placeholder="About company, culture, products..."
                                    required
                                ></textarea>
                            </div>

                            <!-- Offices + Staff -->
                            <div class="row g-3 mb-3">
                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Number of Offices</label
                                    >
                                    <input
                                        type="number"
                                        name="no_of_offices"
                                        class="form-control"
                                        min="1"
                                        placeholder="e.g. 5"
                                        required
                                    />
                                </div>

                                <div class="col-md-6">
                                    <label class="form-label fw-semibold"
                                        >Staff Size</label
                                    >
                                    <input
                                        type="number"
                                        name="staff_size"
                                        class="form-control"
                                        min="1"
                                        placeholder="e.g. 250"
                                        required
                                    />
                                </div>
                            </div>

                            <!-- Password -->
                            <div class="mb-4">
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
                            <div class="d-grid">
                                <button
                                    type="submit"
                                    class="btn btn-primary btn-lg"
                                >
                                    <i class="bi bi-check-circle me-2"></i
                                    >Create Account
                                </button>

                                <p class="text-center mt-3 mb-0">
                                    Already have an account?
                                    <router-link to="/company/login"
                                        >Login</router-link
                                    >
                                </p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
