<template>
    <nav class="navbar navbar-expand-lg border-bottom">
        <div class="container">
            <router-link to="/" class="navbar-brand fw-bold text-primary">
                <i class="bi bi-mortarboard"></i> Placement Portal
            </router-link>

            <ul class="navbar-nav ms-auto align-items-lg-center gap-3">
                <li class="nav-item">
                    <router-link
                        to="/student/login"
                        class="btn btn-outline-primary"
                        >Student Login</router-link
                    >
                </li>
                <li class="nav-item">
                    <router-link to="/company/login" class="btn btn-primary"
                        >Company Login</router-link
                    >
                </li>
                <li class="nav-item">
                    <router-link to="/admin/login" class="btn btn-secondary"
                        >Admin Login</router-link
                    >
                </li>
            </ul>
        </div>
    </nav>

    <!-- HERO -->
    <section class="container my-5">
        <div class="card p-5 shadow-soft">
            <div class="row align-items-center">
                <div class="col-lg-7">
                    <h1 class="fw-bold">
                        One Platform for Campus Hiring & Placements
                    </h1>
                    <p class="text-muted fs-5 mt-3">
                        Connect students, companies, and placement officers with
                        a transparent, efficient hiring workflow.
                    </p>

                    <div class="d-flex gap-3 mt-4">
                        <button class="btn btn-primary btn-lg">
                            <i class="bi bi-search"></i>
                            <router-link
                                to="/student/register"
                                class="text-white"
                                >Explore Jobs</router-link
                            >
                        </button>
                        <button class="btn btn-outline-primary btn-lg">
                            <i class="bi bi-building-add"></i>
                            <router-link
                                to="/company/register"
                                class="text-dark"
                                >Hire talent</router-link
                            >
                        </button>
                    </div>
                </div>

                <div class="col-lg-5 text-center">
                    <i
                        class="bi bi-diagram-3 text-primary"
                        style="font-size: 120px"
                    ></i>
                </div>
            </div>
        </div>
    </section>

    <!-- STATS -->
    <section class="container mb-5">
        <div class="row g-4">
            <div class="col-md-3">
                <div class="card p-4 shadow-soft text-center">
                    <h2 class="fw-bold">150+</h2>
                    <p class="text-muted mb-0">Partner Companies</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-4 shadow-soft text-center">
                    <h2 class="fw-bold">2,400+</h2>
                    <p class="text-muted mb-0">Students Registered</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-4 shadow-soft text-center">
                    <h2 class="fw-bold">320+</h2>
                    <p class="text-muted mb-0">Active Job Openings</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-4 shadow-soft text-center">
                    <h2 class="fw-bold">92%</h2>
                    <p class="text-muted mb-0">Placement Success</p>
                </div>
            </div>
        </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="section-muted py-5">
        <div class="container">
            <h2 class="fw-bold mb-4 text-center">How It Works</h2>

            <div class="row g-4">
                <div class="col-md-6">
                    <div class="card p-4 shadow-soft h-100">
                        <h5 class="fw-semibold">
                            <i class="bi bi-person text-primary"></i> For
                            Students
                        </h5>
                        <ul class="text-muted mt-3">
                            <li>Create academic & skill profile</li>
                            <li>Browse verified campus jobs</li>
                            <li>Apply with one click</li>
                            <li>Track application status</li>
                        </ul>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="card p-4 shadow-soft h-100">
                        <h5 class="fw-semibold">
                            <i class="bi bi-building text-primary"></i> For
                            Companies
                        </h5>
                        <ul class="text-muted mt-3">
                            <li>Register & verify company</li>
                            <li>Post jobs & eligibility criteria</li>
                            <li>View student applications</li>
                            <li>Shortlist & schedule interviews</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FEATURED JOBS -->
    <section class="section-muted py-5">
        <div class="container">
            <h2 class="fw-bold mb-4">Featured Opportunities</h2>

            <div class="row g-4">
                <div class="col-md-4">
                    <div class="card p-4 shadow-soft h-100">
                        <span class="badge badge-soft mb-2">Full Time</span>
                        <h5>Software Engineer</h5>
                        <p class="text-muted mb-1">Google • Bangalore</p>
                        <small class="text-muted">CTC: ₹25 LPA</small>
                        <button class="btn btn-outline-primary w-100 mt-3">
                            Apply
                        </button>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card p-4 shadow-soft h-100">
                        <span class="badge badge-soft mb-2">Internship</span>
                        <h5>Data Analyst</h5>
                        <p class="text-muted mb-1">Amazon • Hyderabad</p>
                        <small class="text-muted">Stipend: ₹50k/month</small>
                        <button class="btn btn-outline-primary w-100 mt-3">
                            Apply
                        </button>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card p-4 shadow-soft h-100">
                        <span class="badge badge-soft mb-2">Graduate User</span>
                        <h5>Associate Consultant</h5>
                        <p class="text-muted mb-1">Deloitte • Pune</p>
                        <small class="text-muted">CTC: ₹8 LPA</small>
                        <button class="btn btn-outline-primary w-100 mt-3">
                            Apply
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="border-top py-4 bg-white">
        <div class="container d-flex justify-content-between">
            <div class="text-muted">Privacy · Terms · Support</div>
        </div>
    </footer>
</template>
