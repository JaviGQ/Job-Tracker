from flask import Flask, render_template, request, redirect
from database import get_db
import json

app = Flask(__name__)

# Homepage
@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Get counts from each table for the dashboard
    cursor.execute("SELECT COUNT(*) as count FROM applications")
    app_count = cursor.fetchone()
    
    conn.close()
    return render_template('dashboard.html', app_count=app_count)

# Companies page (Read)
@app.route('/companies')
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    conn.close()
    return render_template('companies.html', 
                           companies=companies, 
                           mode='list', 
                           selected_company=None)

# Companies Page (Create)
@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company_name = request.form['company_name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO companies (company_name, industry, website, city, state, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (company_name, industry, website, city, state, notes))
        conn.commit()
        conn.close()
        return redirect('/companies')

    # GET - show the add form alongside the list
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    conn.close()
    return render_template('companies.html', 
                           companies=companies, 
                           mode='add', 
                           selected_company=None)

# Companies Page (Update)
@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        company_name = request.form['company_name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']

        cursor.execute("""
            UPDATE companies
            SET company_name=%s, industry=%s, website=%s,
                city=%s, state=%s, notes=%s
            WHERE company_id=%s
        """, (company_name, industry, website, city, state, notes, company_id))
        conn.commit()
        conn.close()
        return redirect('/companies')

    # GET - fetch the company to edit, plus full list
    cursor.execute("SELECT * FROM companies WHERE company_id=%s", (company_id,))
    selected_company = cursor.fetchone()
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    conn.close()
    return render_template('companies.html', 
                           companies=companies, 
                           mode='edit', 
                           selected_company=selected_company)

# Companies Page (Delete)
@app.route('/companies/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id=%s", (company_id,))
    conn.commit()
    conn.close()
    return redirect('/companies')

# Jobs page (Read)
@app.route('/jobs')
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # JOIN lets us show company_name instead of just company_id
    cursor.execute("""
        SELECT jobs.*, companies.company_name 
        FROM jobs 
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.job_title
    """)
    jobs = cursor.fetchall()
    
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    
    conn.close()
    return render_template('jobs.html', 
                           jobs=jobs, 
                           companies=companies,
                           mode='list', 
                           selected_job=None)

# Jobs Page (Create)
@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        company_id = request.form['company_id']
        job_title = request.form['job_title']
        job_type = request.form['job_type']
        salary_min = request.form['salary_min'] or None
        salary_max = request.form['salary_max'] or None
        job_url = request.form['job_url']
        date_posted = request.form['date_posted'] or None

        # For JSON
        requirements = request.form['requirements']
        requirements_json = json.dumps([r.strip() for r in requirements.split(',') if r.strip()])

        cursor.execute("""
            INSERT INTO jobs (company_id, job_title, job_type, salary_min, 
                            salary_max, job_url, date_posted, requirements)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (company_id, job_title, job_type, salary_min, 
              salary_max, job_url, date_posted, requirements_json))
        conn.commit()
        conn.close()
        return redirect('/jobs')

    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    
    cursor.execute("""
        SELECT jobs.*, companies.company_name 
        FROM jobs 
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.job_title
    """)
    jobs = cursor.fetchall()
    conn.close()
    return render_template('jobs.html', 
                           jobs=jobs, 
                           companies=companies,
                           mode='add', 
                           selected_job=None)

# Jobs Page (Update)
@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        company_id = request.form['company_id']
        job_title = request.form['job_title']
        job_type = request.form['job_type']
        salary_min = request.form['salary_min'] or None
        salary_max = request.form['salary_max'] or None
        job_url = request.form['job_url']
        date_posted = request.form['date_posted'] or None
        requirements = request.form['requirements']
        requirements_json = json.dumps([r.strip() for r in requirements.split(',') if r.strip()])

        cursor.execute("""
            UPDATE jobs
            SET company_id=%s, job_title=%s, job_type=%s, salary_min=%s,
                salary_max=%s, job_url=%s, date_posted=%s, requirements=%s
            WHERE job_id=%s
        """, (company_id, job_title, job_type, salary_min,
              salary_max, job_url, date_posted, requirements_json, job_id))
        conn.commit()
        conn.close()
        return redirect('/jobs')

    cursor.execute("SELECT * FROM jobs WHERE job_id=%s", (job_id,))
    selected_job = cursor.fetchone()
    
    if selected_job['requirements']:
        reqs = json.loads(selected_job['requirements'])
        selected_job['requirements_str'] = ', '.join(reqs)
    else:
        selected_job['requirements_str'] = ''

    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()

    cursor.execute("""
        SELECT jobs.*, companies.company_name 
        FROM jobs 
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.job_title
    """)
    jobs = cursor.fetchall()
    conn.close()
    return render_template('jobs.html', 
                           jobs=jobs, 
                           companies=companies,
                           mode='edit', 
                           selected_job=selected_job)

# Jobs Page (Delete)
@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id=%s", (job_id,))
    conn.commit()
    conn.close()
    return redirect('/jobs')

# Applications page (Read)
@app.route('/applications')
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # JOIN across 3 tables to get job title AND company name
    cursor.execute("""
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_date DESC
    """)
    applications = cursor.fetchall()

    for app in applications:
        if app['interview_data']:
            notes = json.loads(app['interview_data'])
            app['interview_notes'] = ', '.join(notes)
        else:
            app['interview_notes'] = 'None'
    
    cursor.execute("""
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY companies.company_name, jobs.job_title
    """)
    jobs = cursor.fetchall()
    
    conn.close()
    return render_template('applications.html',
                           applications=applications,
                           jobs=jobs,
                           mode='list',
                           selected_application=None)

# Applications Page (Create)
@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        job_id = request.form['job_id']
        application_date = request.form['application_date']
        status = request.form['status']
        resume_version = request.form['resume_version']
        cover_letter_sent = 1 if request.form.get('cover_letter_sent') else 0
        interview_notes = request.form['interview_data']
        interview_json = json.dumps([n.strip() for n in interview_notes.split(',') if n.strip()])

        cursor.execute("""
            INSERT INTO applications (job_id, application_date, status,
                                    resume_version, cover_letter_sent, interview_data)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (job_id, application_date, status,
              resume_version, cover_letter_sent, interview_json))
        conn.commit()
        conn.close()
        return redirect('/applications')

    cursor.execute("""
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY companies.company_name, jobs.job_title
    """)
    jobs = cursor.fetchall()

    cursor.execute("""
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_date DESC
    """)
    applications = cursor.fetchall()

    for app in applications:
        if app['interview_data']:
            notes = json.loads(app['interview_data'])
            app['interview_notes'] = ', '.join(notes)
        else:
            app['interview_notes'] = 'None'

    conn.close()
    return render_template('applications.html',
                           applications=applications,
                           jobs=jobs,
                           mode='add',
                           selected_application=None)

# Applications Page (Update)
@app.route('/applications/edit/<int:application_id>', methods=['GET', 'POST'])
def edit_application(application_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        job_id = request.form['job_id']
        application_date = request.form['application_date']
        status = request.form['status']
        resume_version = request.form['resume_version']
        cover_letter_sent = 1 if request.form.get('cover_letter_sent') else 0
        interview_notes = request.form['interview_data']
        interview_json = json.dumps([n.strip() for n in interview_notes.split(',') if n.strip()])

        cursor.execute("""
            UPDATE applications
            SET job_id=%s, application_date=%s, status=%s,
                resume_version=%s, cover_letter_sent=%s, interview_data=%s
            WHERE application_id=%s
        """, (job_id, application_date, status,
              resume_version, cover_letter_sent, interview_json, application_id))
        conn.commit()
        conn.close()
        return redirect('/applications')

    cursor.execute("SELECT * FROM applications WHERE application_id=%s", (application_id,))
    selected_application = cursor.fetchone()

    # Convert JSON back to comma-separated string for the form
    if selected_application['interview_data']:
        notes = json.loads(selected_application['interview_data'])
        selected_application['interview_str'] = ', '.join(notes)
    else:
        selected_application['interview_str'] = ''

    cursor.execute("""
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY companies.company_name, jobs.job_title
    """)
    jobs = cursor.fetchall()

    cursor.execute("""
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_date DESC
    """)
    applications = cursor.fetchall()

    for app in applications:
        if app['interview_data']:
            notes = json.loads(app['interview_data'])
            app['interview_notes'] = ', '.join(notes)
        else:
            app['interview_notes'] = 'None'

    conn.close()
    return render_template('applications.html',
                           applications=applications,
                           jobs=jobs,
                           mode='edit',
                           selected_application=selected_application)

# Applications Page (Delete)
@app.route('/applications/delete/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id=%s", (application_id,))
    conn.commit()
    conn.close()
    return redirect('/applications')

# Contacts page (Read)
@app.route('/contacts')
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.contact_name
    """)
    contacts = cursor.fetchall()
    
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()
    
    conn.close()
    return render_template('contacts.html',
                           contacts=contacts,
                           companies=companies,
                           mode='list',
                           selected_contact=None)

# Contacts Page (Create)
@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        company_id = request.form['company_id']
        contact_name = request.form['contact_name']
        title = request.form['title']
        email = request.form['email']
        phone = request.form['phone']
        linkedin_url = request.form['linkedin_url']
        notes = request.form['notes']

        cursor.execute("""
            INSERT INTO contacts (company_id, contact_name, title,
                                email, phone, linkedin_url, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (company_id, contact_name, title,
              email, phone, linkedin_url, notes))
        conn.commit()
        conn.close()
        return redirect('/contacts')

    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()

    cursor.execute("""
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.contact_name
    """)
    contacts = cursor.fetchall()
    conn.close()
    return render_template('contacts.html',
                           contacts=contacts,
                           companies=companies,
                           mode='add',
                           selected_contact=None)

# Contacts Page (Update)
@app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        company_id = request.form['company_id']
        contact_name = request.form['contact_name']
        title = request.form['title']
        email = request.form['email']
        phone = request.form['phone']
        linkedin_url = request.form['linkedin_url']
        notes = request.form['notes']

        cursor.execute("""
            UPDATE contacts
            SET company_id=%s, contact_name=%s, title=%s,
                email=%s, phone=%s, linkedin_url=%s, notes=%s
            WHERE contact_id=%s
        """, (company_id, contact_name, title,
              email, phone, linkedin_url, notes, contact_id))
        conn.commit()
        conn.close()
        return redirect('/contacts')

    cursor.execute("SELECT * FROM contacts WHERE contact_id=%s", (contact_id,))
    selected_contact = cursor.fetchone()

    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies = cursor.fetchall()

    cursor.execute("""
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.contact_name
    """)
    contacts = cursor.fetchall()
    conn.close()
    return render_template('contacts.html',
                           contacts=contacts,
                           companies=companies,
                           mode='edit',
                           selected_contact=selected_contact)

# Contacts Page (Delete)
@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id=%s", (contact_id,))
    conn.commit()
    conn.close()
    return redirect('/contacts')

if __name__ == '__main__':
    app.run(debug=True)