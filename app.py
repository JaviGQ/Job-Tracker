from flask import Flask, render_template, request, redirect
from database import get_db

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

if __name__ == '__main__':
    app.run(debug=True)