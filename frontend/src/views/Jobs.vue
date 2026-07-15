<script setup>
import JobTable from "../components/JobTable.vue";

import { computed, onMounted, ref } from "vue";
import { api } from "../utils";
import { useRoute } from "vue-router";
import { NotificationStore } from "../stores/NotificationStore";

const route = useRoute();

const statuses = ["All", "Pending", "Approved", "Rejected"];

const notificationStore = NotificationStore();

const jobs = ref([]);

let FilteredJobs = computed(() => {
    let temp = jobs.value;
    if (selectedStatus.value.toLowerCase() != "all") {
        temp = jobs.value.filter(
            (item) =>
                item.approval_status == selectedStatus.value.toLowerCase(),
        );
    }

    if (Query.value.trim() == "") {
        return temp;
    } else {
        console.log("working");
        console.log(Field.value);
        return temp.filter((item) => {
            return item[Field.value]
                .toLowerCase()
                .includes(Query.value.toLowerCase());
        });
    }
});

let endpoint = "jobs/";

if (route.path.includes("company")) {
    endpoint = `company/${route.params.id}/jobs/`;
} else if (route.path.includes("student")) {
    endpoint = `student/${route.params.id}/jobs/`;
}

onMounted(async () => {
    try {
        const res = await api.get(endpoint);
        jobs.value = res.data;
    } catch (err) {
        console.log(err);

        if (err.response) {
            const statusCode = err.response.status;
            if (statusCode == 403) {
                notificationStore.add_message(
                    "danger",
                    "Not Authorized to view The Company's Jobs ",
                );
            }
        }
    }
});
const Field = ref("title");
const Query = ref("");

const selectedStatus = ref("All");
const fields = ["title", "location"];
</script>

<template>
    <div class="d-flex justify-content-between align-items-center m-3">
        <div>
            <h2>{{ title || "Available Jobs" }}</h2>
            <p>{{ subtitle }}</p>
        </div>
    </div>

    <!-- Seaerch Funcationality -->

    <div class="input-group m-3">
        <span class="input-group-text inputGroup-sizing-sm col-2">
            <select v-model="Field" class="form-select">
                <template v-for="field in fields" :key="field">
                    <option :value="field">{{ field }}</option>
                </template>
            </select>
        </span>

        <input
            type="search"
            class="form-control"
            placeholder="Search Jobs"
            v-model="Query"
        />

        <button class="btn btn-light" type="submit">
            <i class="bi bi-search fw-bold text-primary fs-5"></i>
        </button>

        <div class="col-2"></div>
    </div>

    <div class="m-3">
        <ul class="nav nav-pills gap-2">
            <template v-for="status in statuses">
                <li class="nav-item">
                    <a
                        class="nav-link"
                        :class="{ active: status === selectedStatus }"
                        @click="selectedStatus = status"
                    >
                        {{ status }}
                    </a>
                </li>
            </template>
        </ul>
    </div>

    <JobTable :jobs="FilteredJobs"></JobTable>
</template>
