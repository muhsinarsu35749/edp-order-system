from collections import deque

event_queue = deque()
handlers = {}

def subscribe(event_type, handler):
    handlers.setdefault(event_type, []).append(handler)

def publish(event_type, data):
    event_queue.append({"type": event_type, "data": data})

def handle_order_created(data):
    print(f"[Inventory] Reserved '{data['item']}' for Order #{data['order_id']}")
    publish("PAYMENT_PROCESSED", {"order_id": data["order_id"], "amount": data["amount"]})

def handle_payment_processed(data):
    print(f"[Payment] Charged ${data['amount']} for Order #{data['order_id']}")
    publish("ORDER_SHIPPED", {"order_id": data["order_id"]})

def handle_order_shipped(data):
    print(f"[Shipping] Dispatched Order #{data['order_id']}")
    publish("NOTIFICATION_SENT", {"order_id": data["order_id"], "message": "Your order is on the way!"})

def handle_notification_sent(data):
    print(f"[Notification] Order #{data['order_id']}: {data['message']}")

subscribe("ORDER_CREATED", handle_order_created)
subscribe("PAYMENT_PROCESSED", handle_payment_processed)
subscribe("ORDER_SHIPPED", handle_order_shipped)
subscribe("NOTIFICATION_SENT", handle_notification_sent)

publish("ORDER_CREATED", {"order_id": 101, "item": "Mechanical Keyboard", "amount": 85})
publish("ORDER_CREATED", {"order_id": 102, "item": "Wireless Mouse", "amount": 40})

while event_queue:
    event = event_queue.popleft()
    for handler in handlers.get(event["type"], []):
        handler(event["data"])
