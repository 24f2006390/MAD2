import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/Home.vue";
import CompanyDashboard from "./views/CompanyDashboard.vue";
import CompanyPage from "./views/CompanyPage.vue";
import Login from "./views/Login.vue";
import JobPage from "./views/JobPage.vue";
import Jobs from "./views/Jobs.vue";
import JobForm from "./views/job-form.vue";
import CompanyRegisteration from "./views/CompanyRegisteration.vue";
import StudentRegisteration from "./views/StudentRegisteration.vue";
import StudentLogin from "./views/StudentLogin.vue";
import StudentDashboard from "./views/StudentDashboard.vue";
import ApplicationForm from "./views/ApplicationForm.vue";
import Student from "./views/Student.vue";
import Applications from "./views/Applications.vue";
import Application from "./views/Application.vue";
import AdminLogin from "./views/AdminLogin.vue";
import AdminDashboard from "./views/AdminDashboard.vue";
import Students from "./views/Students.vue";
import Companies from "./views/Companies.vue";

const routes = [
  { path: "/applications/", component: Applications },
  { path: "/admin/login/", component: AdminLogin },
  { path: "/admin/dashboard/", component: AdminDashboard },
  { path: "/", component: Home },
  { path: "/students", component: Students },
  { path: "/companies", component: Companies },

  { path: "/company/login/", component: Login },
  { path: "/company/register/", component: CompanyRegisteration },
  { path: "/company/dashboard/", component: CompanyDashboard },
  { path: "/company/:id(\\d+)/", component: CompanyPage },
  { path: "/company/:id(\\d+)/jobs/", component: Jobs },
  { path: "/company/:id(\\d+)/job-form/", component: JobForm },
  { path: "/company/:id(\\d+)/applications/", component: Applications },

  { path: "/job/:id(\\d+)/", component: JobPage },
  { path: "/jobs/", component: Jobs },
  { path: "/job/:id(\\d+)/application-form/", component: ApplicationForm },
  { path: "/job/:id(\\d+)/applications/", component: Applications },

  { path: "/student/register/", component: StudentRegisteration },
  { path: "/student/login/", component: StudentLogin },
  { path: "/student/dashboard/", component: StudentDashboard },
  { path: "/student/:id(\\d+)/jobs/", component: Jobs },
  { path: "/student/:id(\\d+)/", component: Student },
  { path: "/student/:id(\\d+)/applications/", component: Applications },

  { path: "/application/:id(\\d+)/", component: Application },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
