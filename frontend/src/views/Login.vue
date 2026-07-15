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
        const res = await api.post("login/", { ...data, role: "company" });

        console.log(res.data);

        userStore.login(res.data, "company");
        notificationStore.add_message("success", "Company Login Successful");

        console.log("Logged in ");
        console.log(userStore.user);
        console.log(userStore.role);

        router.push("/company/dashboard/");
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
                        <h3 class="mt-2 fw-bold">Company Login</h3>
                    </div>

                    <form
                        @submit.prevent="handle_form_data"
                        action="/api/login/"
                        method="POST"
                    >
                        <div class="mb-3">
                            <label class="form-label fw-semibold">
                                Hr Email
                            </label>

                            <input
                                type="email"
                                name="hr_email"
                                class="form-control"
                                placeholder="hr@company.com"
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
