import random
import mysql.connector
from faker import Faker
from tqdm import tqdm

fake = Faker()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="analytics"
)

cursor = conn.cursor()

NUM_CUSTOMERS = 50000
NUM_ORDERS = 200000

print("Inserting customers...")

for _ in tqdm(range(NUM_CUSTOMERS)):
    name = fake.name()
    city = fake.city()
    signup_date = fake.date_between(start_date='-2y', end_date='today')

    cursor.execute(
        "INSERT INTO customers (name, city, signup_date) VALUES (%s, %s, %s)",
        (name, city, signup_date)
    )

conn.commit()

print("Inserting orders...")

for _ in tqdm(range(NUM_ORDERS)):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    amount = round(random.uniform(10, 1000), 2)
    order_date = fake.date_between(start_date='-1y', end_date='today')

    cursor.execute(
        "INSERT INTO orders (customer_id, amount, order_date) VALUES (%s, %s, %s)",
        (customer_id, amount, order_date)
    )

conn.commit()

cursor.close()
conn.close()

print("Bulk data inserted successfully.")