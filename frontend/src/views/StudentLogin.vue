<script setup>
import { useRouter } from "vue-router";
import { api } from "../utils";
import { CurrentUserStore } from "../stores/CurrentUser";
import { NotificationStore } from "../stores/NotificationStore";

const router = useRouter();

const userStore = CurrentUserStore();
const notificationStore = NotificationStore();

async function handle_form_data(e) {
    const data = Object.fromEntries(new FormData(e.target).entries());

    try {
        const res = await api.post("login/", { ...data, role: "student" });

        userStore.login(res.data, "student");
        notificationStore.add_message("success", "Student Login Successful");
        console.log("Logged in ");

        router.push("/student/dashboard/");
        console.log(userStore.role);
    } catch (err) {
        if (err.response?.status === 403) {
            const data = err.response.data;

            if (data?.status === "banned") {
                router.push("/");
                notificationStore.add_message("danger", "You are banned");
            }
        } else {
            console.log(err);
            notificationStore.add_message("danger", "Invalid Credentials");
        }
    }
}
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5">
                <div class="card login-card shadow-soft p-4 p-md-5">
                    <div class="text-center mb-4">
                        <i
                            class="bi bi-building text-primary"
                            style="font-size: 48px"
                        ></i>
                        <h3 class="mt-2 fw-bold">student Login</h3>
                    </div>

                    <form
                        @submit.prevent="handle_form_data"
                        action="/api/login/"
                        method="POST"
                    >
                        <div class="mb-3">
                            <label class="form-label fw-semibold">
                                Email id
                            </label>

                            <input
                                type="email"
                                name="email_id"
                                class="form-control"
                                placeholder="john@student.com"
                                required
                            />
                        </div>

                        <div class="mb-3">
                            <label class="form-label fw-semibold"
                                >Password</label
                            >
                            <input
                                type="password"
                                name="password"
                                class="form-control"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        <button class="btn btn-primary w-100 py-2 fw-semibold">
                            Login
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
