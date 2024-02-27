from random import randrange
import time
import csv
from faker import Faker

fake = Faker()


def generate_users_csv(row_nb):
    with open("shared/users.csv", "w", newline="\n") as file:
        writer = csv.writer(file)

        for i in range(row_nb):
            writer.writerow([i + 1, fake.first_name(), fake.last_name()])


def generate_products_csv(row_nb):
    with open("shared/products.csv", "w", newline="\n") as file:
        writer = csv.writer(file)

        for i in range(row_nb):
            writer.writerow([i + 1, fake.word(), randrange(0, 1500)])


def generate_follow_csv(row_nb):
    with open("shared/follow.csv", "w", newline="\n") as file:
        writer = csv.writer(file)

        for i in range(1, row_nb + 1):
            for j in range(randrange(0, 21)):
                f = randrange(1, row_nb + 1)
                while i == f:
                    f = randrange(1, row_nb + 1)
                writer.writerow([i, f])


def generate_buy_csv(users_nb, products_nb):
    with open("shared/buy.csv", "w", newline="\n") as file:
        writer = csv.writer(file)

        for i in range(1, users_nb + 1):
            for j in range(randrange(0, 6)):
                writer.writerow([i, randrange(1, products_nb + 1)])


def generate_csv(users_nb, products_nb) -> int:
    print(f"Generate csv.....")
    start_time = time.time()
    generate_users_csv(users_nb)
    generate_products_csv(products_nb)
    generate_follow_csv(users_nb)
    generate_buy_csv(users_nb, products_nb)
    end_time = time.time()
    duration_time = int(end_time - start_time)
    print(f"Finished in {duration_time} seconds")
    return duration_time
