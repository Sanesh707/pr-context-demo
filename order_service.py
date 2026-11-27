import json
from db import database
from cache import redis_client

CACHE_TTL_SECONDS = 300

def get_user_orders(user_id: int):
    cache_key = f"user_orders:{user_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    rows = database.query("""
        SELECT o.id AS order_id, o.total, i.id AS item_id, i.name, i.price
        FROM orders o
        LEFT JOIN order_items i ON o.id = i.order_id
        WHERE o.user_id = ?
    """, [user_id])

    orders_map = {}
    for row in rows:
        oid = row["order_id"]
        if oid not in orders_map:
            orders_map[oid] = {"order_id": oid, "total": row["total"], "items": []}
        if row["item_id"]:
            orders_map[oid]["items"].append({"name": row["name"], "price": row["price"]})

    result = list(orders_map.values())
    redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(result))
    return result
