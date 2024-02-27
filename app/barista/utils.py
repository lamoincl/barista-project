from random import randrange
import time
import csv
from faker import Faker
from neomodel import db

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


def generate_csv(users_nb, products_nb):
    print(f"Generate csv.....")
    start_time = time.time()
    generate_users_csv(users_nb)
    generate_products_csv(products_nb)
    generate_follow_csv(users_nb)
    generate_buy_csv(users_nb, products_nb)
    end_time = time.time()
    print(f"Finished in {int(end_time - start_time)} seconds")


def generate_nodes(user_number=10_000, product_number=100):
    print(f"Generate {user_number:,} users nodes....")
    start_time = time.time()

    query = (
        f"LOAD CSV FROM 'file:///users.csv' AS line\n"
        "CALL {\n"
        "WITH line\n"
        "CREATE (:User {id: toInteger(line[0]), first_name: line[1], last_name: line[2]})\n"
        "} IN TRANSACTIONS"
    )

    rows, _meta = db.cypher_query(query)
    end_time = time.time()
    print(f"Finished in {int(end_time - start_time)} seconds")

    print(f"Generate {product_number:,} products nodes....")
    start_time = time.time()

    query = (
        f"LOAD CSV FROM 'file:///products.csv' AS line\n"
        "CALL {\n"
        "WITH line\n"
        "CREATE (:Product {id: toInteger(line[0]), name: line[1], price: toInteger(line[2])})\n"
        "} IN TRANSACTIONS"
    )

    rows, _meta = db.cypher_query(query)
    end_time = time.time()
    print(f"Finished in {int(end_time - start_time)} seconds")

    
    print(f"Generate follow relation....")
    start_time = time.time()

    query = (
        f"LOAD CSV FROM 'file:///follow.csv' AS line\n"
        "CALL {\n"
        "WITH line\n"
        "MATCH (u:User {id: toInteger(line[0])}), (f:User {id: toInteger(line[1])})\n"
        "CREATE (u)-[:FOLLOW]->(f)\n"
        "} IN TRANSACTIONS"
    )

    rows, _meta = db.cypher_query(query)
    end_time = time.time()
    print(f"Finished in {int(end_time - start_time)} seconds")

    
    print(f"Generate buy relation....")
    start_time = time.time()

    query = (
        f"LOAD CSV FROM 'file:///buy.csv' AS line\n"
        "CALL {\n"
        "WITH line\n"
        "MATCH (u:User {id: toInteger(line[0])}), (p:Product {id: toInteger(line[1])})\n"
        "CREATE (u)-[:BUY]->(p)\n"
        "} IN TRANSACTIONS"
    )

    rows, _meta = db.cypher_query(query)
    end_time = time.time()
    print(f"Finished in {int(end_time - start_time)} seconds")



if __name__ == "__main__":
    generate_nodes()
