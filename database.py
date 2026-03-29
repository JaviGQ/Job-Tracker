import mysql.connector

def get_db():
    """Create and return a database connection."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="job_tracker"
    )
    return connection