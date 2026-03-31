import mysql.connector

def get_db():
    """Create and return a database connection."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD_HERE",
        database="job_tracker"
    )
    return connection