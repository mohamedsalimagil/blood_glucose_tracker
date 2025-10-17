# Blood Glucose Tracker

The Blood Glucose Tracker is a command-line application designed to help users log, view, and manage blood glucose readings. It uses SQLite for persistent storage and follows a modular structure with models, controllers, and utilities.



## Project Structure
.
├── cli.py                 # Handles interactive menu and user commands
├── controllers.py         # Business logic connecting models and CLI actions
├── data/
│   └── blood_glucose.db   # SQLite database file
├── db/
│   ├── __init__.py
│   └── database.py        # Database connection and initialization
├── main.py                # Entry point to start the application
├── models/
│   ├── __init__.py
│   ├── glucose_entry.py   # GlucoseEntry model representing glucose data
│   └── user.py            # User model representing application users
├── requirements.txt       # Python dependencies
├── utils.py               # Helper functions
└── venv/                  # Virtual environment (optional)


## Features
- Create and manage users
- Add blood glucose entries for a user
- View all users
- View glucose entries by user
- Edit glucose entries
- Delete users
- Persistent storage using SQLite

## Installation and Setup
Clone or download the project, then run the following:
cd blood_glucose_tracker
python3 -m venv venv && source venv/bin/activate || venv\Scripts\activate
pip install -r requirements.txt

## Running the Application
python main.py

You will see a menu with options:
1. Create User
2. View All Users
3. Add Glucose Entry
4. View Glucose Entries for a User
5. Delete User
6. Edit Glucose Entry
0. Exit

## Database
The database file is located at data/blood_glucose.db. It is created automatically if it does not exist.

## Requirements
Install all dependencies with:
pip install -r requirements.txt

## License (MIT)

## Author
Mohamed Salim Agil

