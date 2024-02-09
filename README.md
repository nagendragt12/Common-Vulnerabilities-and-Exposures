
# Project Title

A brief description of what this project does and who it's for

Introduction
Welcome to o Common
Vulnerabilities and Exposures (CVEs) This Flask project is designed to brief description of project purpose. It utilizes Flask, a lightweight WSGI web application framework in Python.

Installation

1. Clone the repository: 
```
git clone https://github.com/nagendragt12/project.git
```
2. Navigate to the project directory:
```
cd <project_directory>
```
3. Create a virtual environment:
```
python -m venv .venv
```
4. Activate the virtual environment:

 window:
```
.venv\Scripts\activate
```
5. Install Flask:
```
pip install Flask
```
6. Install python-dotenv for environment variable management:
```
pip install python-dotenv
```
7. Install psycopg2-binary for PostgreSQL database connection:
```
pip install psycopg2-binary
```
Usage
1. Running the Flask App:

To start the Flask app in development mode, run:
```
flask run
```
2. Database Connection:

Create a PostgreSQL database.

Obtain the database URL.

Set up a .env file in the project directory and add the database URL:
```
DATABASE_URL=<database_url>
```
Configure the Flask app to read the database URL from the .env file using python-dotenv

3. Importing Data from CSV:

Prepare your CSV file containing the CVE data.
Place the CSV file in the project directory.
Update the app.py file to read data from the CSV file, create the table, and insert data into the PostgreSQL database.
4. Executing the Main Function:

Execute the app.py script to import data from the CSV file into the PostgreSQL database:
```
python app.py
```
Endpoints:

- `GET /cve/<cve_id>`: Retrieve details of a CVE by its ID.
- `GET /cve`: Retrieve details of all CVEs.
- `POST /cve`: Add a new CVE record.
- `DELETE /cve/<cve_id>`: Delete a CVE record by its ID.
- `PUT /cve/<cve_id>`: Modify details of a CVE record by its ID.
