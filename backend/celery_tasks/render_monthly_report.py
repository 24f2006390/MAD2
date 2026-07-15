from celery_tasks.get_monthly_report_data import (
    application_stats,
    overview,
    pending_companies,
    pending_counts,
    pending_jobs,
    pending_students,
    start,
    top_companies,
    top_jobs,
)

monthly_report_html = f"""
<h1>Placement Portal Monthly Report</h1>

<p>
Reporting Period:
<b>{start.strftime("%B %Y")}</b>
</p>

<h2>Overview</h2>

<table border="1" cellpadding="8">
    <tr>
        <th>Metric</th>
        <th>Value</th>
    </tr>

    <tr>
        <td>New Students</td>
        <td>{overview["new_students"]}</td>
    </tr>

    <tr>
        <td>New Companies</td>
        <td>{overview["new_companies"]}</td>
    </tr>

    <tr>
        <td>New Jobs</td>
        <td>{overview["new_jobs"]}</td>
    </tr>

    <tr>
        <td>Applications</td>
        <td>{overview["applications"]}</td>
    </tr>

    <tr>
        <td>Selected</td>
        <td>{overview["selected"]}</td>
    </tr>

    <tr>
        <td>Shortlisted</td>
        <td>{overview["shortlisted"]}</td>
    </tr>

    <tr>
        <td>Rejected</td>
        <td>{overview["rejected"]}</td>
    </tr>

    <tr>
        <td>Pending</td>
        <td>{overview["pending"]}</td>
    </tr>
</table>
"""


monthly_report_html += f"""
<hr>

<h2>Pending Approvals</h2>

<table border="1" cellpadding="8">
<tr>
    <th>Category</th>
    <th>Count</th>
</tr>

<tr>
    <td>Students</td>
    <td>{pending_counts["students"]}</td>
</tr>

<tr>
    <td>Companies</td>
    <td>{pending_counts["companies"]}</td>
</tr>

<tr>
    <td>Jobs</td>
    <td>{pending_counts["jobs"]}</td>
</tr>

</table>
"""

monthly_report_html += """
<h3>Latest Pending Students</h3>

<table border="1" cellpadding="6">
<tr>
    <th>Name</th>
    <th>Branch</th>
    <th>Graduation</th>
</tr>
"""

for student in pending_students:
    monthly_report_html += f"""
    <tr>
        <td>{student.first_name} {student.last_name}</td>
        <td>{student.branch}</td>
        <td>{student.graduation_year}</td>
    </tr>
    """

monthly_report_html += "</table>"


monthly_report_html += """
<h3>Latest Pending Companies</h3>

<table border="1" cellpadding="6">
<tr>
    <th>Name</th>
    <th>Industry</th>
</tr>
"""

for company in pending_companies:
    monthly_report_html += f"""
    <tr>
        <td>{company.name}</td>
        <td>{company.industry}</td>
    </tr>
    """

monthly_report_html += "</table>"


monthly_report_html += """
<h3>Latest Pending Jobs</h3>

<table border="1" cellpadding="6">
<tr>
    <th>Company</th>
    <th>Title</th>
    <th>Location</th>
</tr>
"""

for job in pending_jobs:
    monthly_report_html += f"""
    <tr>
        <td>{job.company.name}</td>
        <td>{job.title}</td>
        <td>{job.location}</td>
    </tr>
    """

monthly_report_html += "</table>"


monthly_report_html += """
<hr>

<h2>Top Hiring Companies</h2>

<table border="1" cellpadding="6">
<tr>
    <th>Rank</th>
    <th>Company</th>
    <th>Applications</th>
</tr>
"""

for i, company in enumerate(top_companies, start=1):
    monthly_report_html += f"""
    <tr>
        <td>{i}</td>
        <td>{company.name}</td>
        <td>{company.applications}</td>
    </tr>
    """

monthly_report_html += "</table>"


monthly_report_html += """
<hr>

<h2>Most Popular Jobs</h2>

<table border="1" cellpadding="6">
<tr>
    <th>Rank</th>
    <th>Job</th>
    <th>Company</th>
    <th>Applications</th>
</tr>
"""

for i, job in enumerate(top_jobs, start=1):
    monthly_report_html += f"""
    <tr>
        <td>{i}</td>
        <td>{job.title}</td>
        <td>{job.company}</td>
        <td>{job.applications}</td>
    </tr>
    """

monthly_report_html += "</table>"


monthly_report_html += """
<hr>

<h2>Application Statistics</h2>

<table border="1" cellpadding="6">

<tr>
    <th>Metric</th>
    <th>Value</th>
</tr>

"""

monthly_report_html += f"""
<tr>
<td>Total Applications</td>
<td>{application_stats["total"]}</td>
</tr>

<tr>
<td>Pending</td>
<td>{application_stats["pending"]}</td>
</tr>

<tr>
<td>Shortlisted</td>
<td>{application_stats["shortlisted"]}</td>
</tr>

<tr>
<td>Selected</td>
<td>{application_stats["selected"]}</td>
</tr>

<tr>
<td>Rejected</td>
<td>{application_stats["rejected"]}</td>
</tr>

<tr>
<td>Selection Rate</td>
<td>{application_stats["selection_rate"]}%</td>
</tr>

<tr>
<td>Shortlisting Rate</td>
<td>{application_stats["shortlisting_rate"]}%</td>
</tr>

</table>
"""
