<script setup>
import { computed, ref } from "vue";
import { CurrentUserStore } from "../stores/CurrentUser";
import router from "../router";
import { storeToRefs } from "pinia";

const userStore = CurrentUserStore();
const { role, user } = storeToRefs(userStore);

const logged_in = computed(() => !!userStore.user);

const jobLabel = computed(() => {
    if (userStore.role === "student") return "Applied";
    if (userStore.role === "company") return "My";
    return "All";
});

function logout() {
    userStore.logout();
    router.push("/");
}

let applications_endpoint = computed(() => {
    if (role.value != "admin") {
        return `/${role.value}/${user.value.id}/applications/`;
    } else {
        return "/applications/";
    }
});

let job_endpoint = computed(() => {
    if (role.value != "admin") {
        return `/${role.value}/${user.value.id}/jobs/`;
    } else {
        return "/jobs/";
    }
});
</script>

<template>
    <nav class="navbar card">
        <div class="container-fluid bg-white">
            <div class="navbar-brand">
                <i class="bi bi-buildings text-primary"></i>
                <router-link to="/" class="text-decoration-none">
                    <span class="text-primary fw-bold">Placement Portal</span>
                </router-link>
            </div>

            <template v-if="logged_in">
                <div class="me-auto nav fs-6">
                    <div class="nav-item">
                        <router-link
                            :to="`/${userStore.role}/dashboard/`"
                            class="nav-link text-muted"
                        >
                            <i class="bi bi-grid me-2"></i>
                            Dashboard
                        </router-link>
                    </div>

                    <div class="nav-item">
                        <router-link
                            :to="job_endpoint"
                            class="nav-link text-muted"
                        >
                            <i class="bi bi-briefcase me-2"></i>
                            {{ jobLabel }}
                            Jobs
                        </router-link>
                    </div>

                    <div class="nav-item">
                        <router-link
                            :to="applications_endpoint"
                            class="nav-link text-muted"
                        >
                            <i class="bi bi-file-text me-2"></i>

                            Applications
                        </router-link>
                    </div>

                    <div v-if="role == 'admin'" class="nav-item">
                        <router-link to="/students" class="nav-link text-muted">
                            <i class="bi bi-people me-2"></i>

                            All Students
                        </router-link>
                    </div>

                    <div v-if="role == 'admin'" class="nav-item">
                        <router-link
                            to="/companies"
                            class="nav-link text-muted"
                        >
                            <i class="bi bi-buildings me-2"></i>
                            All Companies
                        </router-link>
                    </div>
                </div>
            </template>

            <div v-if="userStore.role == 'student'" class="nav-item me-3">
                <router-link
                    :to="`/student/${userStore.user.id}/`"
                    class="nav-link text-muted"
                >
                    <i class="bi bi-person-circle me-1"></i>
                    Profile
                </router-link>
            </div>

            <div class="nav-item">
                <button @click="logout" class="nav-link text-danger">
                    <i class="bi bi-box-arrow-right me-1"></i>
                    Logout
                </button>
            </div>
        </div>
    </nav>
</template>
