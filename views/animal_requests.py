import sqlite3
import json
from models import Animal
from models import Location
from models import Customer


def get_all_animals():
    """ Gets all animals """
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
       SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id, 
            a.customer_id,  
            l.name AS location_name,
            l.address AS location_address,
            c.name AS customer_name,
            c.address AS customer_address,
            c.email AS customer_email,
            c.password AS customer_password
        FROM Animal a
        JOIN Location l ON l.id = a.location_id
        JOIN Customer c ON c.id = a.customer_id""")


        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create a Location instance from the current row
            location = Location(
                row['location_id'],
                row['location_name'],
                row['location_address']
            )

            # Create a Customer instance from the current row
            customer = Customer(
                row['customer_id'],
                row['customer_name'],
                row['customer_address'],
                row['customer_email'],
                row['customer_password']
            )

            # Create an animal instance from the current row
            animal = Animal(
                row['id'],
                row['name'],
                row['breed'],
                row['status'],
                row['customer_id'],  # Swap location_id with customer_id
                row['location_id'],  # Swap customer_id with location_id
            )

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__

            # Add the dictionary representation of the customer to the animal
            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    return animals



def get_single_animal(id):
    """ Gets a single animal and additional details """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM Animal a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                        data['status'], data['location_id'],
                        data['customer_id'])

        return animal.__dict__


def create_animal(new_animal):
    """ Creates new animal """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'],  new_animal['breed'],
              new_animal['status'], new_animal['locationId'],
              new_animal['customerId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowidD

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return new_animal



def delete_animal(id):
    """ Deletes animal """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Animal
        WHERE id = ?
        """, (id, ))


def update_animal(id, new_animal):
    """ Updates an animal """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['locationId'],
              new_animal['customerId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def get_animal_by_location(location_id):
    """ Gets an animal by their location_id """

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.status,
            a.breed,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.location_id = ?
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Animal(
                row['id'], row['name'], row['status'], row['breed'],
                row['location_id'], row['customer_id'])
            animals.append(customer.__dict__)

    return animals


def get_animal_by_status(status):
    """ Gets a customer by their status """

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.status,
            a.breed,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.status = ?
        """, (status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'], row['name'], row['status'], row['breed'],
                row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)

    return animals
