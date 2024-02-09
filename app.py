from flask import Flask, jsonify,request
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
        cve_dict = {
        'cve_id': cve[1],
        'severity': cve[2],
        'cvss': cve[3],
        'affected_packages': cve[4],
        'description': cve[5],
        'cwe_id': cve[6]
        }
        return jsonify(cve_dict), 200
    else:
        return jsonify({'error': 'CVE ID not found'}), 4044
    

@app.route('/cve', methods=['GET'])
def get_cve_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cve_database')
    cves = cursor.fetchall()
    conn.close()
    if cves:
        cves_list = []
        for cve in cves:
            cve_dict = {
            'cve_id': cve[1],
            'severity': cve[2],
            'cvss': cve[3],
            'affected_packages': cve[4],
            'description': cve[5],
            'cwe_id': cve[6]
            }
            cves_list.append(cve_dict)
        return jsonify(cves_list), 200
    else:
        return jsonify({'error': 'CVE ID not found'}), 404
    

@app.route('/cve', methods=['POST'])
def add_cve():
    # Extract data from the request payload
    cve_data = request.json
    
    # Check if the required fields are present in the request payload
    required_fields = ['cve_id', 'severity', 'cvss', 'affected_packages', 'description', 'cwe_id']
    if not all(field in cve_data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Insert the new CVE record into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO cve_database (cve_id, severity, cvss, affected_packages, description, cwe_id) VALUES (%s, %s, %s, %s, %s, %s)',
                       (cve_data['cve_id'], cve_data['severity'], cve_data['cvss'], cve_data['affected_packages'], cve_data['description'], cve_data['cwe_id']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'CVE record added successfully'}), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': f'Failed to add CVE record: {str(e)}'}), 500
    
@app.route('/cve/<cve_id>', methods=['DELETE'])
def delete_cve(cve_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM cve_database WHERE cve_id = %s', (cve_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': f'CVE record with ID {cve_id} deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': f'Failed to delete CVE record with ID {cve_id}: {str(e)}'}), 500
@app.route('/cve/<cve_id>', methods=['PUT'])
def modify_cve(cve_id):
    # Extract data from the request payload
    cve_data = request.json

    # Check if the required fields are present in the request payload
    required_fields = ['severity', 'cvss', 'affected_packages', 'description', 'cwe_id']
    if not all(field in cve_data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Update the details of the specified CVE record
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE cve_database SET severity = %s, cvss = %s, affected_packages = %s, description = %s, cwe_id = %s WHERE cve_id = %s',
                       (cve_data['severity'], cve_data['cvss'], cve_data['affected_packages'], cve_data['description'], cve_data['cwe_id'], cve_id))
        conn.commit()
        conn.close()
        return jsonify({'message': f'CVE record with ID {cve_id} modified successfully'}), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': f'Failed to modify CVE record with ID {cve_id}: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)