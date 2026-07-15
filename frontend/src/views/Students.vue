<script setup>
import StudentTable from "../components/StudentTable.vue";

import { computed, onMounted, ref } from "vue";
import { api } from "../utils";
import { useRoute } from "vue-router";

const route = useRoute();

const statuses = ["All", "Pending", "Approved", "Rejected"];

const students = ref([]);

let FilteredStudents = computed(() => {
    let temp = students.value;
    if (selectedStatus.value.toLowerCase() != "all") {
        temp = students.value.filter(
            (item) =>
                item.approval_status == selectedStatus.value.toLowerCase(),
        );
    }

    function handle_field(item, field_name) {
        if (field_name == "name") {
            return item.first_name + item.last_name;
        }
        return item[field_name];
    }

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

let endpoint = "students/";

if (route.path.includes("company")) {
    endpoint = `company/${route.params.id}/students/`;
}

onMounted(async () => {
    try {
        const res = await api.get(endpoint);
        students.value = res.data;
    } catch (err) {
        console.log(err);
    }
});
const Field = ref("name");
const fields = ["name", "branch", "degree", "graduation_year", "email_id"];

const Query = ref("");
const selectedStatus = ref("All");
</script>

<template>
    <div class="d-flex justify-content-between align-items-center m-3">
        <div>
            <h2>{{ title || "Available Students" }}</h2>
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
            placeholder="Search Students"
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

    <StudentTable :students="FilteredStudents"></StudentTable>
</template>
