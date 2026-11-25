 Hotel Reservation Management System

Python Peer Review Project – Group 8

Institution: JAIN (Deemed-to-be University)
Department: CTIS
Semester: III
Academic Year: 2026–2027

---

 Project Overview

The Hotel Reservation Management System is a Python-based console application developed to simplify hotel operations, including customer registration, room management, reservation processing, availability checking, and billing.

The project demonstrates the practical implementation of Python programming concepts, particularly Object-Oriented Programming (OOP), inheritance, polymorphism, exception handling, data structures, and JSON file handling.

 Objectives

- Simplify hotel room reservation operations.
- Maintain customer information with unique identification numbers.
- Manage room availability and booking details.
- Prevent overlapping reservations.
- Calculate room charges based on room categories.
- Maintain records using JSON file storage.

 Key Features

- Customer Management: Register customers and generate unique Customer IDs.
- Room Management: Display room categories, prices, and available services.
- Room Availability: Search rooms based on room type and reservation dates.
- Reservation Management: Create, view, and cancel reservations.
- Booking Validation: Prevent overlapping bookings for the same room.
- Dynamic Billing: Calculate charges using polymorphism.
- Data Persistence: Store customer, room, and reservation records in JSON files.
- Exception Handling: Handle invalid inputs and booking errors.

 Technologies Used

Technology| Purpose
Python 3.10+| Core programming language
JSON| Data storage and management
UUID| Unique customer and reservation IDs
Datetime| Date validation and reservation management
Pathlib| File and directory management
OOP| Structured application development

 Python Concepts Implemented

- Classes and Objects
- Encapsulation
- Inheritance
- Polymorphism
- Dictionaries and Lists
- Custom Exception Handling
- File Handling
- Data Validation

 System Architecture

The application is organized into the following major components:

1. Room Management: Handles different room categories and their services.
2. Customer Management: Maintains customer details and unique identification.
3. Reservation Management: Processes bookings, cancellations, and availability checks.
4. Billing System: Calculates charges according to room category and duration.
5. JSON Storage: Maintains application data between executions.

 Installation and Execution

Prerequisites

- Python 3.10 or later
- Visual Studio Code or any Python-supported IDE

Steps to Run

1. Clone the repository

git clone https://github.com/rohan-neel7/Group8_Hotel_Reservation_Management_System.git

2. Navigate to the project directory

cd Group8_Hotel_Reservation_Management_System

3. Run the Python application

python3 peer_review.py

The application automatically creates the required JSON data files when executed for the first time.

 Application Menu

The system provides the following operations:

Option| Operation
1| Display Hotel Rooms
2| Search Available Rooms
3| Register New Customer
4| Book a Hotel Room
5| View All Reservations
6| Search Customer
7| Cancel Reservation
8| Exit Application

 Billing Mechanism

The system uses polymorphism to calculate room charges according to the selected room category.

- Standard Room: Base room price per night.
- Deluxe Room: Base price plus amenities charges.
- Suite: Base price plus amenities charges, with a 10% discount for stays of three or more nights.

 Data Management and Validation

The application uses JSON files to store room details, customer records, and reservation information.

It also implements:

- Customer detail validation.
- Check-in and check-out date validation.
- Room availability verification.
- Prevention of overlapping reservations.
- Reservation cancellation validation.

 Future Enhancements

- Graphical User Interface (GUI).
- Database integration using MySQL or SQLite.
- Online payment gateway integration.
- Customer login and administrator authentication.
- Automated invoice generation.
- Email and SMS reservation notifications.

 Project Information

Project Name: Hotel Reservation Management System
Project Group: Group 8
Project Type: Python Peer Review
Domain: Hotel Management and Reservation Automation

 Conclusion

The Hotel Reservation Management System demonstrates the application of Python programming concepts in developing a practical hotel management solution. It provides an organized approach to customer registration, room reservations, availability management, billing, and data storage.

The project strengthens understanding of Object-Oriented Programming and real-world software development practices.

---

Developed as part of the Python Peer Review Project – Group 8.
