# FLY — Airport Management System

Software Engineering 2026, University of Trento — Team **Mooka**
Alawadi Mohammed Redha Osama Majeed, Conte Giorgia, Fanara Gaspare Francesco Luigi, Ranieri Vittoria

FLY is a web application developed for the management of airport services and operations. The system provides dedicated functionality for clients, airline personnel, ground staff, and administrators through a role-based access control model; airport information, flight schedules, amenities, assistance requests, staff management, and operational monitoring are handled through a Flask application backed by an SQLite database. The application follows a three-tier architecture composed of a Jinja2 presentation layer, a Flask application layer, and an SQLite data layer.

## Technology Stack

The application has been implemented using Python 3 and Flask, with SQLite as the persistence layer. The frontend is rendered server-side through Jinja2 templates and styled using plain CSS. Data access is performed through explicit SQL queries rather than an ORM.

## Running the Application

Create and activate a virtual environment, install the dependencies, initialize the database, optionally populate it with sample data, and start the Flask development server.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

python -m pip install -r requirements.txt

python -m flask --app app init-db
python seed.py

python -m flask --app app run
```

Once started, the application is available at:

```text
http://127.0.0.1:5000
```

The seed script creates demonstration accounts and reference data for testing purposes. Staff accounts use the password:

```text
password
```

## Demo Data and Accounts

After initializing the database, running `python seed.py` populates the application with sample data for demonstration and testing purposes.

The script creates the following demo accounts:

| Role | Name | Email | Password |
|------|------|-------|----------|
| Administrator | Ada Admin | admin@fly.local | password |
| Airline Manager | Mara Manager | manager@ita.local | password |
| Airline Staff | Sam Schedule | staff@ita.local | password |
| Ground Operations Manager | Gio Ground | ground@fly.local | password |
| Operations Staff | Otto Ops | ops@fly.local | password |
| Client | Cleo Client | cleo@example.com | OAuth login |

The client account uses the application's mocked OAuth authentication flow and does not require a password.

In addition to user accounts, the seed script creates:
- Two airlines:
  - ITA Airways
  - Lufthansa
- Three airport amenities:
  - Fast Track Security
  - Lounge Access
  - Priority Line
- Airport information content:
  - Parking information
  - Security regulations
- One terminal (`T1`) with two gates (`A1`, `A2`)
- One aircraft assigned to ITA Airways
- One flight schedule (`AZ123`) with a generated departure instance
- One published shift assigned to the operations staff account

This data is intended only for local testing and demonstration of the implemented functionalities.

Client authentication is performed through the application's mocked OAuth flow.

## Implemented Functionality

The current implementation covers account creation and authentication, airport information access, amenity purchases, assistance requests, profile management, flight schedule management, weather and shift visualization, aircraft movement tracking, accountability logging, and administrative staff management. Several use cases related to advanced ground operations and emergency procedures are represented in the domain model but remain outside the implemented prototype.

## Project Structure

```text
FLY/
├── app.py                 # Flask application factory
├── config.py              # Application configuration
├── database/
│   ├── db.py              # Database connection utilities
│   └── schema.sql         # Relational schema definition
├── models/                # Domain model classes
├── routes/                # Flask blueprints and business logic
├── templates/             # Jinja2 templates
├── static/                # CSS resources
├── seed.py                # Sample data generation
├── requirements.txt       # Python dependencies
├── Doxyfile               # Doxygen configuration
└── README.md
```

## Architecture Overview

The application follows a three-tier architecture. Requests are received by Flask blueprints, business logic is executed within the application layer, data is retrieved or updated through SQLite, and responses are rendered through Jinja2 templates before being returned to the browser. Authentication, authorization, and role-based access control are enforced through shared route decorators.

## Documentation

Source code documentation can be generated through Doxygen:

```bash
doxygen Doxyfile
```

The generated documentation is written to:

```text
docs/doxygen/html/
```

Additional implementation details, user flows, architectural decisions, and use-case coverage are documented in the project report.