import psycopg2
import csv


# Function to create table
def create_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS cve_database (
                        id SERIAL PRIMARY KEY,
                        cve_id TEXT,
                        severity TEXT,
                        cvss TEXT,
                        affected_packages TEXT,
                        description TEXT,
                        cwe_id TEXT
                   )''')


# Function to insert data into the table
def insert_data(cursor, data):
    cursor.executemany('''INSERT INTO cve_database(cve_id , severity ,cvss  ,affected_packages ,description , cwe_id) 
                          VALUES (%s, %s, %s, %s, %s, %s)''', data)


# Function to read data from CSV
def read_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            data.append(tuple(row))
    return data


# Main function
def main():
    # Define your CSV file path
    csv_file = 'C:\\Users\\naga\\Downloads\\CVE_DATABASE.csv'

    # Connect to PostgreSQL database
    conn = psycopg2.connect("postgres://jfvzwkju:BzUzsrjF212Xqzl7NjPs-1E9axG7OqUv@rain.db.elephantsql.com/jfvzwkju")
    cursor = conn.cursor()

    # Create table if not exists
    create_table(cursor)

    # Read data from CSV
    data = read_csv(csv_file)

    # Insert data into the table
    insert_data(cursor, data)

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
