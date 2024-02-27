import time
from neomodel import db, clear_neo4j_database


def inject_csv():
    print("Generate users nodes....")
    start_time = time.time()

    query = (
        f"LOAD CSV FROM 'file:///users.csv' AS line\n"
        "CALL {\n"
        "WITH line\n"
        "CREATE (:User {id: toInteger(line[0]), first_name: line[1], last_name: line[2]})\n"
        "} IN TRANSACTIONS"
    )
    db.cypher_query(query)

    print("Generate products nodes....")
    query = (
        f"LOAD CSV FROM 'file:///products.csv' AS line\n"
        "CALL {\n"
        "WITH line\n"
        "CREATE (:Product {id: toInteger(line[0]), name: line[1], price: toInteger(line[2])})\n"
        "} IN TRANSACTIONS"
    )
    db.cypher_query(query)

    print(f"Generate follow relation....")
    query = (
        f"LOAD CSV FROM 'file:///follow.csv' AS line\n"
        "CALL {\n"
        "WITH line\n"
        "MATCH (u:User {id: toInteger(line[0])}), (f:User {id: toInteger(line[1])})\n"
        "CREATE (u)-[:FOLLOW]->(f)\n"
        "} IN TRANSACTIONS"
    )
    db.cypher_query(query)

    print(f"Generate buy relation....")
    query = (
        f"LOAD CSV FROM 'file:///buy.csv' AS line\n"
        "CALL {\n"
        "WITH line\n"
        "MATCH (u:User {id: toInteger(line[0])}), (p:Product {id: toInteger(line[1])})\n"
        "CREATE (u)-[:BUY]->(p)\n"
        "} IN TRANSACTIONS"
    )
    db.cypher_query(query)
    end_time = time.time()
    duration_time = int(end_time - start_time)
    print(f"Finished in {duration_time} seconds")
    return duration_time


def init_neo4j():
    clear_neo4j_database(db, True, True)
    db.cypher_query("CREATE INDEX user_id_index FOR (n:User) ON (n.id)")
    db.cypher_query("CREATE INDEX product_id_index FOR (n:Product) ON (n.id)")
    return inject_csv()


def request1(user_id: int, max_level: int = 4):
    params = {"id": user_id}
    query = (
        f"MATCH path=(s:User {{id: $id}})<-[:FOLLOW*1..{int(max_level)}]-(f)\n"
        "WITH DISTINCT f, LENGTH(path) AS level\n"
        "MATCH (f)-[:BUY]->(p)\n"
        "WITH level, p, COUNT(p) AS orders\n"
        "RETURN level, orders, p.id AS productId, p.name AS productName\n"
        "ORDER BY level, orders DESC"
    )
    return db.cypher_query(query, params)


def request2(product_id: int, user_id: int, max_level: int = 4):
    params = {"productId": product_id, "userId": user_id}
    query = (
        f"PROFILE MATCH path=(s:User {{id: $userId}})<-[:FOLLOW*1..{int(max_level)}]-(f)\n"
        "WITH DISTINCT f, LENGTH(path) AS level\n"
        "MATCH (f)-[:BUY]->(p:Product {id: $productId})\n"
        "WITH level, p, COUNT(p) AS orders\n"
        "RETURN level, orders, p.id AS productId, p.name AS productName\n"
        "ORDER BY level, orders DESC"
    )
    return db.cypher_query(query, params)


def request3(product_id: int, max_level: int = 4):
    params = {"productId": product_id}
    query = (
        "MATCH (p:Product {id: $productId})<-[:BUY]-(u:User)\n"
        f"MATCH path=(u)<-[:FOLLOW*1..{max_level}]-(follower)\n"
        "WHERE (follower)-[:BUY]->(p)\n"
        "RETURN LENGTH(path) AS level, COUNT(DISTINCT follower) AS viralCount\n"
        "ORDER BY level"
    )
    return db.cypher_query(query, params)
