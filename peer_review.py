"""
GROUP 8 - HOTEL RESERVATION MANAGEMENT SYSTEM
Python Peer Review Project
JAIN (Deemed-to-be University) | Semester III

Features:
- Room management and availability
- Customer registration and unique IDs
- Reservation creation and cancellation
- Date-overlap validation
- Polymorphic room billing
- JSON data persistence
"""

import json
import uuid
from pathlib import Path
from datetime import datetime


# ---------------- CUSTOM EXCEPTIONS ----------------

class HotelError(Exception):
    pass


class ValidationError(HotelError):
    pass


class RoomUnavailableError(HotelError):
    pass


class RoomNotFoundError(HotelError):
    pass


# ---------------- ROOM MODEL AND INHERITANCE ----------------

class Room:
    def __init__(self, number, price, amenities=0):
        self.number = number
        self.price = price
        self.amenities = amenities

    def calculate_charge(self, nights):
        return self.price * nights

    def get_services(self):
        return ("Wi-Fi", "TV")

    def to_dict(self):
        return {
            "number": self.number,
            "price": self.price,
            "amenities": self.amenities,
            "type": self.__class__.__name__
        }


class StandardRoom(Room):
    def calculate_charge(self, nights):
        return self.price * nights


class DeluxeRoom(Room):
    def calculate_charge(self, nights):
        return (self.price + self.amenities) * nights

    def get_services(self):
        return ("Wi-Fi", "Breakfast", "Mini-Bar")


class Suite(Room):
    def calculate_charge(self, nights):
        total = (self.price + self.amenities) * nights
        return total * 0.90 if nights >= 3 else total

    def get_services(self):
        return ("Wi-Fi", "Breakfast", "Mini-Bar", "Premium Lounge")


ROOM_TYPES = {
    "StandardRoom": StandardRoom,
    "DeluxeRoom": DeluxeRoom,
    "Suite": Suite
}


# ---------------- CUSTOMER MODEL ----------------

class Customer:
    def __init__(self, name, phone, email=""):
        self.customer_id = "C" + uuid.uuid4().hex[:8].upper()
        self.name = name.strip().title()
        self.phone = phone
        self.email = email.strip().lower()

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }


# ---------------- RESERVATION MODEL ----------------

class Reservation:
    def __init__(self, customer_id, room_number,
                 check_in, check_out, total):
        self.reservation_id = "R" + uuid.uuid4().hex[:8].upper()
        self.customer_id = customer_id
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out
        self.total_charge = total
        self.status = "CONFIRMED"

    def to_dict(self):
        return self.__dict__.copy()


# ---------------- JSON STORAGE ----------------

class JsonStorage:
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)

        self.files = {
            "rooms": self.data_dir / "rooms.json",
            "customers": self.data_dir / "customers.json",
            "reservations": self.data_dir / "reservations.json"
        }

        defaults = {
            "rooms": [
                {"number": 101, "price": 2000, "amenities": 0,
                 "type": "StandardRoom"},
                {"number": 102, "price": 2200, "amenities": 0,
                 "type": "StandardRoom"},
                {"number": 201, "price": 3200, "amenities": 300,
                 "type": "DeluxeRoom"},
                {"number": 202, "price": 3500, "amenities": 300,
                 "type": "DeluxeRoom"},
                {"number": 301, "price": 5500, "amenities": 700,
                 "type": "Suite"}
            ],
            "customers": [],
            "reservations": []
        }

        for key, path in self.files.items():
            if not path.exists():
                self.save(key, defaults[key])

    def load(self, key):
        try:
            with open(self.files[key], "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            raise HotelError(f"Unable to read {key} data: {error}")

    def save(self, key, data):
        try:
            with open(self.files[key], "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except OSError as error:
            raise HotelError(f"Unable to save {key} data: {error}")


# ---------------- HOTEL BUSINESS LOGIC ----------------

class HotelService:
    def __init__(self):
        self.storage = JsonStorage()
        self.rooms = {}
        self.customers = {}
        self.reservations = {}
        self.load_data()

    def load_data(self):
        for item in self.storage.load("rooms"):
            room_class = ROOM_TYPES.get(item["type"], StandardRoom)
            room = room_class(
                item["number"], item["price"], item["amenities"]
            )
            self.rooms[room.number] = room

        for item in self.storage.load("customers"):
            self.customers[item["customer_id"]] = item

        for item in self.storage.load("reservations"):
            self.reservations[item["reservation_id"]] = item

    def save_customers(self):
        self.storage.save("customers", list(self.customers.values()))

    def save_reservations(self):
        self.storage.save(
            "reservations", list(self.reservations.values())
        )

    @staticmethod
    def validate_dates(check_in, check_out):
        try:
            start = datetime.strptime(check_in, "%Y-%m-%d").date()
            end = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Dates must use YYYY-MM-DD format.")

        if start < datetime.today().date():
            raise ValidationError("Check-in cannot be in the past.")

        if end <= start:
            raise ValidationError(
                "Check-out must be after check-in."
            )

        return (end - start).days

    def register_customer(self, name, phone, email=""):
        if len(name.strip()) < 2:
            raise ValidationError("Enter a valid customer name.")

        if not phone.isdigit() or not 7 <= len(phone) <= 15:
            raise ValidationError(
                "Phone number must contain 7 to 15 digits."
            )

        if email and ("@" not in email or email.startswith("@")):
            raise ValidationError("Enter a valid email address.")

        customer = Customer(name, phone, email)
        self.customers[customer.customer_id] = customer.to_dict()
        self.save_customers()
        return customer

    def search_customers(self, name):
        return [
            customer for customer in self.customers.values()
            if name.strip().lower() in customer["name"].lower()
        ]

    def is_available(self, room_number, check_in, check_out):
        for reservation in self.reservations.values():
            if (
                reservation["room_number"] == room_number
                and reservation["status"] == "CONFIRMED"
                and check_in < reservation["check_out"]
                and check_out > reservation["check_in"]
            ):
                return False
        return True

    def search_rooms(self, room_type, check_in, check_out):
        self.validate_dates(check_in, check_out)

        return [
            room for room in self.rooms.values()
            if room_type.lower() in room.__class__.__name__.lower()
            and self.is_available(room.number, check_in, check_out)
        ]

    def create_reservation(self, customer_id, room_number,
                           check_in, check_out):

        nights = self.validate_dates(check_in, check_out)

        if customer_id not in self.customers:
            raise ValidationError("Customer ID not found.")

        if room_number not in self.rooms:
            raise RoomNotFoundError("Room number does not exist.")

        if not self.is_available(room_number, check_in, check_out):
            raise RoomUnavailableError(
                "Room is already booked for these dates."
            )

        room = self.rooms[room_number]
        total = room.calculate_charge(nights)

        reservation = Reservation(
            customer_id, room_number, check_in, check_out, total
        )

        self.reservations[reservation.reservation_id] = (
            reservation.to_dict()
        )
        self.save_reservations()

        return reservation

    def cancel_reservation(self, reservation_id):
        reservation = self.reservations.get(reservation_id)

        if not reservation:
            raise ValidationError("Reservation ID not found.")

        if reservation["status"] == "CANCELLED":
            raise ValidationError("Reservation is already cancelled.")

        reservation["status"] = "CANCELLED"
        self.save_reservations()
        return reservation


# ---------------- DISPLAY FUNCTIONS ----------------

def display_rooms(hotel):
    print("\n" + "=" * 65)
    print("                  HOTEL ROOM DIRECTORY")
    print("=" * 65)

    for room in hotel.rooms.values():
        print(
            f"Room: {room.number} | "
            f"Type: {room.__class__.__name__} | "
            f"Price: Rs.{room.price:.2f} | "
            f"Amenities: Rs.{room.amenities:.2f}"
        )
        print("Services:", ", ".join(room.get_services()))


def display_reservations(hotel):
    print("\n" + "=" * 65)
    print("                  RESERVATION RECORDS")
    print("=" * 65)

    if not hotel.reservations:
        print("No reservations found.")
        return

    for reservation in hotel.reservations.values():
        print(
            f"ID: {reservation['reservation_id']} | "
            f"Customer: {reservation['customer_id']} | "
            f"Room: {reservation['room_number']} | "
            f"Dates: {reservation['check_in']} to "
            f"{reservation['check_out']} | "
            f"Amount: Rs.{reservation['total_charge']:.2f} | "
            f"Status: {reservation['status']}"
        )


# ---------------- MAIN APPLICATION ----------------

def main():
    hotel = HotelService()

    print("\n" + "=" * 65)
    print("       GROUP 8 - HOTEL RESERVATION MANAGEMENT SYSTEM")
    print("=" * 65)

    while True:
        print("""
1. Display Hotel Rooms
2. Search Available Rooms
3. Register New Customer
4. Book a Hotel Room
5. View All Reservations
6. Search Customer
7. Cancel Reservation
8. Exit
""")

        choice = input("Enter your choice (1-8): ").strip()

        try:
            if choice == "1":
                display_rooms(hotel)

            elif choice == "2":
                room_type = input("Enter room type (Standard/Deluxe/Suite): ")
                check_in = input("Check-in (YYYY-MM-DD): ")
                check_out = input("Check-out (YYYY-MM-DD): ")

                rooms = hotel.search_rooms(
                    room_type, check_in, check_out
                )

                if rooms:
                    print("\nAvailable Rooms:")
                    for room in rooms:
                        print(
                            f"{room.number} - "
                            f"{room.__class__.__name__} - "
                            f"Rs.{room.price}/night"
                        )
                else:
                    print("No available rooms found.")

            elif choice == "3":
                name = input("Customer Name: ")
                phone = input("Phone Number: ")
                email = input("Email (optional): ")

                customer = hotel.register_customer(name, phone, email)

                print("\nCustomer Registered Successfully!")
                print("Customer ID:", customer.customer_id)

            elif choice == "4":
                customer_id = input("Customer ID: ").strip().upper()
                room_number = int(input("Room Number: "))
                check_in = input("Check-in (YYYY-MM-DD): ")
                check_out = input("Check-out (YYYY-MM-DD): ")

                reservation = hotel.create_reservation(
                    customer_id, room_number, check_in, check_out
                )

                print("\nBOOKING CONFIRMED!")
                print("Reservation ID:", reservation.reservation_id)
                print("Total Amount: Rs.", reservation.total_charge)

            elif choice == "5":
                display_reservations(hotel)

            elif choice == "6":
                name = input("Enter customer name to search: ")
                results = hotel.search_customers(name)

                if results:
                    for customer in results:
                        print(customer)
                else:
                    print("No matching customers found.")

            elif choice == "7":
                reservation_id = input("Enter Reservation ID: ").strip().upper()
                hotel.cancel_reservation(reservation_id)
                print("Reservation cancelled successfully.")

            elif choice == "8":
                print("\nThank you for using our Hotel Management System!")
                print("All records have been saved.")
                break

            else:
                print("Invalid choice. Please select 1 to 8.")

        except (HotelError, ValueError) as error:
            print("\nERROR:", error)

        except KeyboardInterrupt:
            print("\nApplication interrupted.")
            break


if __name__ == "__main__":
    main()