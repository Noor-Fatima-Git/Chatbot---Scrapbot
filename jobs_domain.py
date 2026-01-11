# ================= JOBS DATABASE =================
jobs_db = {
    "software engineer": [
        {"company": "Systems Ltd", "city": "islamabad", "salary": 150000},
        {"company": "NetSol", "city": "rawalpindi", "salary": 120000}
    ],
    "teacher": [
        {"company": "Beaconhouse", "city": "islamabad", "salary": 60000}
    ],
    "accountant": [
        {"company": "Private Firm", "city": "rawalpindi", "salary": 80000}
    ],

    # ➕ NEW JOBS
    "graphic designer": [
        {"company": "Creative Agency", "city": "islamabad", "salary": 70000}
    ],
    "data analyst": [
        {"company": "TechSoft", "city": "lahore", "salary": 130000}
    ]
}

# ================= JOB HANDLER =================
def handle_jobs(user_input, context):
    text = user_input.lower()

    # extract job role
    job = next((j for j in jobs_db if j in text), None)

    # extract city (optional)
    cities = ["islamabad", "rawalpindi", "lahore"]
    city = next((c for c in cities if c in text), None)

    if not job:
        return (
            "What job are you looking for?\n"
            "Software Engineer, Teacher, Accountant, Graphic Designer or Data Analyst?",
            "jobs"
        )

    results = jobs_db.get(job, [])

    if city:
        results = [r for r in results if r["city"] == city]

    if not results:
        return "Sorry, no jobs found for your criteria.", None

    reply = f"Job openings for **{job.title()}**:\n"
    for r in results:
        reply += (
            f"- {r['company']} ({r['city'].title()}) "
            f"– Salary: PKR {r['salary']}\n"
        )

    return reply.strip(), None
