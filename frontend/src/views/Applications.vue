<script setup>
import ApplicationTable from "../components/ApplicationTable.vue";

import { computed, onMounted, ref } from "vue";
import { api } from "../utils";
import { useRoute } from "vue-router";
import { NotificationStore } from "../stores/NotificationStore";

const route = useRoute();

const statuses = ["All", "pending", "shortlisted", "selected", "rejected"];

const notificationStore = NotificationStore();

const applications = ref([]);

let FilteredApplications = computed(() => {
    let temp = applications.value;

    // filter applications based on status
    if (selectedStatus.value.toLowerCase() != "all") {
        temp = applications.value.filter(
            (item) => item.status == selectedStatus.value.toLowerCase(),
        );
    }

    //  handle search logic

    const handle_field = (item, field_name) => {
        if (field_name == "student_name") {
            return item.student.first_name + item.student.last_name;
        } else if (field_name == "company_name") {
            return item.job.company.name;
        } else if (field_name == "job_name") {
            return item.job.title;
        }
    };

    if (Query.value.trim() == "") {
        return temp;
    } else {
        console.log("working");
        console.log(Field.value);
        return temp.filter((item) => {
            return handle_field(item, Field.value)
                .toLowerCase()
                .includes(Query.value.toLowerCase());
        });
    }
});

let endpoint = "applications/";

if (route.path.includes("company")) {
    endpoint = `company/${route.params.id}/applications/`;
} else if (route.path.includes("student")) {
    endpoint = `student/${route.params.id}/applications/`;
} else if (route.path.includes("job")) {
    endpoint = `job/${route.params.id}/applications/`;
}

onMounted(async () => {
    try {
        const res = await api.get(endpoint);
        applications.value = res.data;
        console.log(applications.value);
    } catch (err) {
        console.log(err);
        if (err.response) {
            const statusCode = err.response.status;
            if (statusCode == 403) {
                notificationStore.add_message(
                    "danger",
                    "Not Authorized to view these applicatons  ",
                );
            }
        }
    }
});
const Field = ref("student_name");
const Query = ref("");

const selectedStatus = ref("All");
const fields = ["student_name", "company_name", "job_name"];
</script>

<template>
    <div class="d-flex justify-content-between align-items-center m-3">
        <div>
            <h2>{{ title || "Available Applications" }}</h2>
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
            placeholder="Search Applications"
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

    <ApplicationTable :applications="FilteredApplications"></ApplicationTable>
</template>
