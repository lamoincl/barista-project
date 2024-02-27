MATCH (p:Product {id: $productId})<-[:BUY]-(u:User)
MATCH path=(u)<-[:FOLLOW*1..4]-(follower)
WHERE (follower)-[:BUY]->(p)
RETURN LENGTH(path) AS level, COUNT(DISTINCT follower) AS viralCount
ORDER BY level