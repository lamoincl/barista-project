from barista.utils import generate_nodes


generate_nodes()


# PROFILE MATCH path=(s:NeoUser {uid: "2a05d72951a94145b29f428d71634ab3"})<-[:FOLLOW*1..8]-(f)
# WITH DISTINCT f, LENGTH(path) AS level
# MATCH (f)-[:BUY]->(p)
# WITH level, p, COUNT(p) AS orders
# RETURN level, orders, p.uid AS productId, p.name AS productName
# ORDER BY level, orders DESC

# CREATE INDEX product_id_index FOR (n:Product) ON (n.id)
# CREATE INDEX user_id_index FOR (n:User) ON (n.id)