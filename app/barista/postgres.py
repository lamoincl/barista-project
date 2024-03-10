import time
from django.db import connection
from django.core.management import call_command


def inject_csv():
    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute("""
            COPY social_users_postgresuser(id, first_name, last_name)
            FROM '/barista/users.csv'
            DELIMITER ',';
        """)
        cursor.execute("""
            COPY products_postgresproduct(id, name, price)
            FROM '/barista/products.csv'
            DELIMITER ',';
        """)
        cursor.execute("""
            COPY social_users_postgresuser_users(from_postgresuser_id, to_postgresuser_id)
            FROM '/barista/follow.csv'
            DELIMITER ',';
        """)
        cursor.execute("""
            COPY social_users_postgresuser_products(postgresuser_id, postgresproduct_id)
            FROM '/barista/buy.csv'
            DELIMITER ',';
        """)
    end_time = time.time()
    return int(end_time - start_time)

def init_postgres():
    call_command("flush", interactive=False)
    with connection.cursor() as cursor:
        cursor.execute("""
CREATE INDEX idx_social_users_postgresuser_id ON social_users_postgresuser(id);
CREATE INDEX idx_social_users_postgresuser_users_from_id ON social_users_postgresuser_users(from_postgresuser_id);
CREATE INDEX idx_social_users_postgresuser_users_to_id ON social_users_postgresuser_users(to_postgresuser_id);
CREATE INDEX idx_social_users_postgresuser_products_user_id ON social_users_postgresuser_products(postgresuser_id);
CREATE INDEX idx_social_users_postgresuser_products_product_id ON social_users_postgresuser_products(postgresproduct_id);
CREATE INDEX idx_products_postgresproduct_id ON products_postgresproduct(id);
""")
    return inject_csv()

def request1(user_id: int, max_level: int = 4):
    query = (
        """
        WITH RECURSIVE UserConnections AS (
    SELECT
        1 AS Level,
        f.from_postgresuser_id AS followerId
    FROM
        social_users_postgresuser s
    INNER JOIN social_users_postgresuser_users f ON s.id = f.to_postgresuser_id
    WHERE
        s.id = %s
    UNION ALL
    SELECT
        uc.Level + 1,
        f.from_postgresuser_id
    FROM
        UserConnections uc
    INNER JOIN social_users_postgresuser_users f ON uc.followerId = f.to_postgresuser_id
    WHERE
        uc.Level < %s
),
Purchases AS (
    SELECT
        uc.Level,
        b.postgresproduct_id,
        COUNT(b.postgresproduct_id) AS orders
    FROM
        UserConnections uc
    INNER JOIN social_users_postgresuser_products b ON uc.followerId = b.postgresuser_id
    GROUP BY
        uc.Level, b.postgresproduct_id
),
ProductDetails AS (
    SELECT
        p.id AS productId,
        p.name AS productName,
        p.*
    FROM
        products_postgresproduct p
)
SELECT
    p.Level,
    p.orders,
    pd.productId,
    pd.productName
FROM
    Purchases p
INNER JOIN ProductDetails pd ON p.postgresproduct_id = pd.productId
ORDER BY
    p.Level, p.orders DESC;

        """
    )
    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id, max_level])
        rows = cursor.fetchall()
    end_time = time.time()
    return int(end_time - start_time), rows, ("level", "orders", "productId", "productName")

def request2(product_id: int, user_id: int, max_level: int = 4):
    query = """
    WITH RECURSIVE UserConnections AS (
    SELECT
        1 AS Level,
        f.from_postgresuser_id AS followerId
    FROM
        social_users_postgresuser s
    INNER JOIN social_users_postgresuser_users f ON s.id = f.to_postgresuser_id
    WHERE
        s.id = %s
    UNION ALL
    SELECT
        uc.Level + 1,
        f.from_postgresuser_id
    FROM
        UserConnections uc
    INNER JOIN social_users_postgresuser_users f ON uc.followerId = f.to_postgresuser_id
    WHERE
        uc.Level < %s
),
Purchases AS (
    SELECT
        uc.Level,
        b.postgresuser_id,
        COUNT(*) AS orders
    FROM
        UserConnections uc
    INNER JOIN social_users_postgresuser_products b ON uc.followerId = b.postgresuser_id
    WHERE
        b.postgresproduct_id = %s
    GROUP BY
        uc.Level, b.postgresuser_id
)
SELECT
    p.Level,
    p.orders,
    prod.id AS productId,
    prod.name AS productName
FROM
    Purchases p
INNER JOIN products_postgresproduct prod ON prod.id = %s
ORDER BY
    p.Level, p.orders DESC;
    """
    
    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id, max_level, product_id, product_id])
        rows = cursor.fetchall()
    end_time = time.time()
    return int(end_time - start_time), rows, ("level", "orders", "productId", "productName")


def request3(product_id: int, max_level: int = 4):
    query = """
    WITH RECURSIVE FollowerPath AS (
    SELECT
        u.id AS userId,
        f.from_postgresuser_id AS followerId,
        1 AS Level
    FROM
        social_users_postgresuser u
    INNER JOIN social_users_postgresuser_users f ON u.id = f.to_postgresuser_id
    INNER JOIN social_users_postgresuser_products b ON u.id = b.postgresuser_id
    WHERE
        b.postgresproduct_id = %s
    UNION ALL
    SELECT
        fp.userId,
        f.from_postgresuser_id,
        fp.Level + 1
    FROM
        FollowerPath fp
    INNER JOIN social_users_postgresuser_users f ON fp.followerId = f.to_postgresuser_id
    WHERE
        fp.Level < %s
),
ViralFollowers AS (
    SELECT
        fp.Level,
        fp.followerId
    FROM
        FollowerPath fp
    INNER JOIN social_users_postgresuser_products b ON fp.followerId = b.postgresuser_id
    WHERE
        b.postgresproduct_id = %s
)
SELECT
    Level,
    COUNT(DISTINCT followerId) AS viralCount
FROM
    ViralFollowers
GROUP BY
    Level
ORDER BY
    Level;

    """
    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute(query, [product_id, max_level, product_id])
        rows = cursor.fetchall()
    end_time = time.time()
    return int(end_time - start_time), rows, ("level", "viralCount")

