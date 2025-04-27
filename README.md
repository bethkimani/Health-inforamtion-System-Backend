# Health-inforamtion-System-Backend
Center for Epidemiological Modelling and Analysis (CEMA) Project

The  cema Health Information System is a backend application designed for managing client health information and health programs. Built with Flask and SQLite, this application allows healthcare providers to efficiently register clients, manage health programs, and keep track of client health records.



## Table of Contents
Features
Technologies Used
Installation
API Documentation
Code Structure
Best Practices
Testing
Contributing
License
Acknowledgments
Features



### Goals or what i was supposed to implement

Create Health Programs: Admins can create various health programs (e.g., TB, Malaria, HIV).



Register Clients: Add new clients with comprehensive profiles.



Enroll Clients: Enroll clients in multiple health programs.



Search and View Clients: Easily search for clients and view their profiles.



API Access: Expose client profiles via API for integration with other systems.

Technologies Used





Flask: A lightweight web framework for building APIs.



Flask-SQLAlchemy: ORM for managing database interactions.



Flask-JWT-Extended: For secure JWT-based authentication.



Flask-CORS: To enable Cross-Origin Resource Sharing.



SQLite: A lightweight database for data storage.

Installation



## Clone the Repository:

git clone git@github.com:bethkimani/Health-inforamtion-System-Backend.git
cd health-information-system-backend



## Set Up a Virtual Environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`



## Install Dependencies:

pip install -r requirements.txt



## Configure the Application:





## Update the config.py file with your database configurations and secret keys.



## Run Database Migrations:

flask db init
flask db migrate
flask db upgrade



## Start the Server:

flask run  || python3 app.py ||python app.py

### API Documentation

## Authentication
POST /api/login: Authenticate users and retrieve a JWT token.



POST /api/register: Register a new user (JWT required).

## Clients

GET /api/clients: Retrieve all clients.

POST /api/clients: Register a new client.

GET /api/clients/: View a client’s profile.

PUT /api/clients/: Update a client’s information.

DELETE /api/clients/: Remove a client from the system.

## Health Programs


GET /api/programs: Retrieve all health programs.

POST /api/programs: Create a new health program.

DELETE /api/programs/: Delete a health program.

## Health Records


GET /api/health-records: Retrieve all health records.


PATCH /api/health-records//complete: Mark a health record as completed.

Appointments


GET /api/appointments: Retrieve all appointments.

PATCH /api/appointments//approve: Approve an appointment.

PATCH /api/appointments//reject: Reject an appointment.

 ## Code Structure

health-information-system-backend/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── auth.py
│   ├── client.py
│   ├── program.py
│   ├── health_record.py
│   └── appointment.py
│
├── config.py
├── requirements.txt
└── run.py



## Best Practices

Clean Code: Followed PEP 8 guidelines for Python code.

Modular Design: Organized code into blueprints for maintainability.

Error Handling: Comprehensive error handling and logging throughout the application.

## Testing

use a testing framework like pytest to validate functionality.

Write tests for each endpoint to ensure data integrity and response accuracy.

## Contributing
Contributions are welcome! Please submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Thanks to the Flask community for their resources and support.
Inspired by best practices in RESTful API design and development.