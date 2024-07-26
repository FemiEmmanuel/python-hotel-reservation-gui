# Hotel Reservation System

A comprehensive hotel reservation system built with Python, featuring a graphical user interface using custom tkinter and MySQL database integration.

## Features

- User-friendly GUI for easy navigation and booking
- Real-time room availability checking
- Database storage for reservations
- Invoice generation and management
- Admin panel for hotel management

## Prerequisites

- Python 3.8+
- MySQL 8.0+

## Setup Instructions

1. Ensure you have Python and MySQL installed on your system.
2. Clone the repository: git clone https://github.com/FemiEmmanuel/python-hotel-reservation-gui, cd python-hotel-reservation-gui
3. Create a virtual environment: python -m venv venv. To activate run: venv/bin/activate  # On Windows use  venv\Scripts\activate
4. Install required packages: pip install -r requirements.txt
5. Set up the MySQL database: Create config.py file in the root folder and create a dictionary as db_config with your database credentials.
6. Run the database initialization script: python database.py

## Usage

Run the main application: python main.py

## Project Structure

- `main.py`: Entry point of the application
- `gui/`: Contains all GUI-related classes and functions
- `models/`: Database models and business logic

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

Oluwafemi Olorunyolemi - phenox08@gmail.com

Project Link: [https://github.com/FemiEmmanuel/python-hotel-reservation-gui](https://github.com/FemiEmmanuel/python-hotel-reservation-gui)
