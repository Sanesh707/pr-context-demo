from db import database

def get_user_orders(user_id: int):
    orders = database.query("SELECT * FROM orders WHERE user_id = ?", [user_id])
    results = []
    for order in orders:
        items = database.query("SELECT * FROM order_items WHERE order_id = ?", [order.id])
        results.append({
            "order_id": order.id,
            "total": order.total,
            "items": items
        })
    return results
