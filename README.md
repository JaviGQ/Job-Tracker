# Job Application Tracker

A full-stack web application for tracking job applications, built with 
MySQL, Python/Flask, and HTML/CSS.

## Features

- **Dashboard** — Overview of application statistics and recent activity
- **Companies** — Track companies you are interested in or have applied to
- **Jobs** — Manage job postings with requirements and salary information
- **Applications** — Track application status, resume versions, and interview notes
- **Contacts** — Store recruiter and hiring manager contact information
- **Job Match** — Enter your skills and get ranked job matches by compatibility

## Technologies Used

- **Database:** MySQL 8.0
- **Backend:** Python 3 / Flask
- **Frontend:** HTML, CSS, Chart.js
- **Version Control:** GitHub

---

## Prerequisites

### Windows
- Python 3.x — https://www.python.org/downloads/
- MySQL Server 8.0 — https://dev.mysql.com/downloads/mysql/
- MySQL Workbench (recommended) — https://dev.mysql.com/downloads/workbench/
- Git Bash — https://git-scm.com/downloads

### Linux (Ubuntu/Debian)
- Python 3 and pip
- python3-venv and python3-full
- MySQL Server 8.0

Install all Linux prerequisites with:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-full python3-venv mysql-server
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd job_tracker
```

---

### 2. Set Up a Virtual Environment

#### Windows (Git Bash)
```bash
python -m venv venv
source venv/Scripts/activate
```

#### Linux / Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

You will know the virtual environment is active when you see `(venv)` 
at the start of your terminal prompt.

---

### 3. Install Dependencies

With your virtual environment active:
```bash
pip install -r requirements.txt
```

---

### 4. Set Up MySQL

#### Windows
- Open the Services panel (`Win + R` → type `services.msc`)
- Find **MySQL80** and make sure it is **Running**
- If not, right click it and select **Start**

#### Linux (Ubuntu)
Start the MySQL service:
```bash
sudo service mysql start
```

Enable it to start automatically on boot:
```bash
sudo systemctl enable mysql
```

---

### 5. Initialize the Database

#### Windows (Git Bash) or Linux
Navigate to your project folder and run:
```bash
mysql -u root -p < schema.sql
```

#### Alternative — MySQL Workbench
1. Open MySQL Workbench and connect to your local server
2. Click **File → Open SQL Script** and select `schema.sql`
3. Click the lightning bolt ⚡ button to execute
4. Confirm all 4 tables were created under the `job_tracker` database

#### Verify the Database Was Created
```bash
mysql -u root -p -e "USE job_tracker; SHOW TABLES;"
```

You should see all four tables listed:
```
+-----------------------+
| Tables_in_job_tracker |
+-----------------------+
| applications          |
| companies             |
| contacts              |
| jobs                  |
+-----------------------+
```

---

### 6. Configure Database Credentials

Open `database.py` and update the connection details with your 
MySQL credentials:
```python
def get_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD_HERE",  # add your MySQL password here
        database="job_tracker"
    )
    return connection
```

---

### 7. Run the Application

Make sure your virtual environment is active (you should see `(venv)` 
in your prompt), then run:
```bash
python app.py
```

On Linux you may need:
```bash
python3 app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

---

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

- **companies** — Company information including industry and location
- **jobs** — Job postings linked to companies with requirements stored as JSON
- **applications** — Application records linked to jobs with status tracking
- **contacts** — Contact people linked to companies