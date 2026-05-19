# TransTrack

TransTrack is a desktop-based transport operations management system built with Python, Tkinter, MongoDB, and PyMongo. It centralizes the daily records used by a transport company, including owners, vehicles, drivers, conductors, stage managers, routes, trips, collections, expenses, deductions, payouts, users, audit logs, and detailed reports.

The system is designed for a transport company that needs better visibility into operations, finances, vehicle assignments, staff records, and owner payouts.

## Features

- Admin dashboard with quick access to all major modules
- Owner management for vehicle owner records and statuses
- Vehicle management with owner, route, insurance, inspection, and status details
- Driver and conductor management with assigned vehicle tracking
- Stage manager management for stage coordination
- Route management with origins, destinations, stages, fare structure, and expected revenue
- Trip management for scheduled, departed, in-transit, and completed trips
- Collection tracking for trip revenue
- Expense tracking for operational costs
- Deduction tracking for owner-related deductions
- Payout processing for owner earnings, deductions, and net payouts
- User management with roles and linked records
- Audit logging for important system actions
- Detailed reports that fetch data across the full system

## User Roles

TransTrack supports the following roles:

- Admin
- Operations Manager
- Vehicle Owner
- Driver
- Conductor
- Stage Manager

Each role is intended to support a different part of the transport workflow, while the admin has access to the complete system.

## Technology Stack

- Python
- Tkinter for the desktop graphical user interface
- MongoDB for data storage
- PyMongo for MongoDB access
- python-dotenv for environment variable loading
- bcrypt for password hashing
- fpdf2 and Pillow for report/document support

## Project Structure

```text
transtrack/
  app.py
  config.py
  controllers/
  db/
  models/
  utils/
  views/
main.py
requirements.txt
.env.example
```

### Main Folders

- `models/` defines the data structures used by the system.
- `controllers/` handles business logic, validation, and database operations.
- `views/` contains the Tkinter user interface screens.
- `db/` handles MongoDB connection and indexes.
- `utils/` contains shared helpers for sessions, security, auditing, validation, IDs, relationships, and numbers.

## Requirements

Before running the system, make sure you have:

- Python 3.10 or later
- MongoDB running locally or a MongoDB Atlas connection string
- Git, if cloning the project from a repository

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root.

You can copy the values from `.env.example`:

```text
TRANSTRACK_MONGO_URI=mongodb://localhost:27017/
TRANSTRACK_MONGO_TIMEOUT_MS=10000
```

For MongoDB Atlas, use your Atlas connection string instead:

```text
TRANSTRACK_MONGO_URI=mongodb+srv://<db_username>:<db_password>@<cluster-url>/?retryWrites=true&w=majority
TRANSTRACK_MONGO_TIMEOUT_MS=10000
```

## Running the Application

Start the app from the project root:

```bash
python main.py
```

When the app starts, it checks the MongoDB connection, creates database indexes, creates a seed admin account if the users collection is empty, and opens the TransTrack desktop interface.

## Default Login

If the database has no users, the system creates a default admin account:

```text
Username: admin
Password: admin123
```

For security, change this password or create a new admin user after the first login.

## Main Workflow

1. Register vehicle owners.
2. Register vehicles and link them to owners.
3. Register drivers, conductors, and stage managers.
4. Create routes with stages and expected revenue.
5. Schedule and manage trips.
6. Record collections from trips.
7. Record expenses and deductions.
8. Process owner payouts.
9. Review detailed reports and audit logs.

## Reports

The Reports module provides a detailed view of data across the whole system. It includes:

- Overview metrics and record coverage
- Trip status, vehicle status, and user role breakdowns
- Detailed trip, collection, route, and stage manager reports
- Financial summaries, expenses, deductions, and payouts
- Owner, vehicle, driver, and conductor reports
- User records and audit logs

This helps administrators and operations staff understand both daily activity and overall company performance.

## Database Collections

TransTrack stores data in the `transtrack_db` MongoDB database using collections such as:

- `users`
- `owners`
- `vehicles`
- `drivers`
- `conductors`
- `stage_managers`
- `routes`
- `trips`
- `collections`
- `expenses`
- `deductions`
- `payouts`
- `audit_logs`

## Security and Accountability

The system includes:

- Password hashing
- Login and logout sessions
- Active and inactive user statuses
- Role-based user records
- Linked users for owners, drivers, conductors, and stage managers
- Audit logs for system actions such as login, logout, create, update, and delete

## Validation

TransTrack validates important records before saving them. Validation includes:

- Required fields
- Existing linked records
- Date formats
- Future and non-future date rules
- Numeric amounts
- Unique indexes for key fields such as usernames, vehicle plates, owner national IDs, and driver license numbers

## Future Improvements

Possible improvements include:

- PDF and Excel report exports
- Cloud deployment
- Web-based version
- Mobile version
- SMS and email notifications
- Advanced analytics charts
- Automated payout schedules
- Backup and restore tools
- More detailed permission controls
- Integration with payment platforms

## Author

John Muchikuri Kinya

## License

This project is for learning and academic demonstration purposes.
