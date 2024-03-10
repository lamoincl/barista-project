MATCH path=(s:User {id: $userId})<-[:FOLLOW*1..4]-(f)
WITH DISTINCT f, LENGTH(path) AS level
MATCH (f)-[:BUY]->(p:Product {id: $productId})
WITH level, p, COUNT(p) AS orders
RETURN level, orders, p.id AS productId, p.name AS productName
ORDER BY level, orders DESC