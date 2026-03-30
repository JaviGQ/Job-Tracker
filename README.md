# Job Application Tracker

A full-stack web application for tracking job applications, built with MySQL, Python/Flask, and HTML/CSS.

## Features

- **Dashboard** — Overview of application statistics and recent activity
- **Companies** — Track companies you are interested in or have applied to
- **Jobs** — Manage job postings with requirements and salary information
- **Applications** — Track application status, resume versions, and interview notes
- **Contacts** — Store recruiter and hiring manager contact information
- **Job Match** — Enter your skills and get ranked job matches by compatibility

## Technologies Used

- **Database:** MySQL
- **Backend:** Python 3 / Flask
- **Frontend:** HTML, CSS, Chart.js
- **Version Control:** GitHub

## Prerequisites

Before running this application make sure you have the following installed:

- Python 3.x
- MySQL Server
- pip

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd job_tracker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up the Database

Log into MySQL and run the schema file:
```bash
mysql -u root -p < schema.sql
```

Or open MySQL Workbench, open `schema.sql`, and execute it.

### 4. Configure Database Credentials

Open `database.py` and update the connection details with your MySQL credentials:
```python
def get_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD_HERE",
        database="job_tracker"
    )
    return connection
```

### 5. Run the Application
```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure
```
job_tracker/
├── app.py              # Main Flask application and routes
├── database.py         # Database connection
├── schema.sql          # Database schema — run to initialize
├── requirements.txt    # Python dependencies
├── AI_USAGE.md         # GenAI documentation
├── README.md           # Project documentation
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── companies.html
│   ├── jobs.html
│   ├── applications.html
│   ├── contacts.html
│   └── job_match.html
└── static/
    └── style.css
```

## Database Schema

The application uses four related tables:

- **companies** — Company information
- **jobs** — Job postings linked to companies
- **applications** — Application records linked to jobs
- **contacts** — Contact people linked to companies