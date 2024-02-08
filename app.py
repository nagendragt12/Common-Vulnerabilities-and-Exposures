from flask import Flask, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
#postgres://jfvzwkju:BzUzsrjF212Xqzl7NjPs-1E9axG7OqUv@rain.db.elephantsql.com/jfvzwkju
# Database connection configuration
DATABASE = 'postgres://jfvzwkju:BzUzsrjF212Xqzl7NjPs-1E9axG7OqUv@rain.db.elephantsql.com/jfvzwkju'  # PostgreSQL database connection string

# Function to establish database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE)
    conn.autocommit = True
    return conn

# API Endpoint for retrieving CVE details by ID
@app.route('/cve/<cve_id>', methods=['GET'])
def get_cve(cve_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cve_database WHERE cve_id = %s', (cve_id,))
    cve = cursor.fetchone()
    conn.close()
    if cve:
        column_names = ['cve_id', 'severity', 'cvss', 'affected_packages', 'description', 'cwe_id']
        cve_dict = dict(zip(column_names, cve))
        return jsonify(cve_dict), 200
    else:
        return jsonify({'error': 'CVE ID not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)