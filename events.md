# Events

This document lists all events used in the Event-Driven Order Processing System.

## 1. `ORDER_CREATED`
- **Producer:** Main application (initial order trigger)
- **Payload:** `{"order_id": int, "item": str, "amount": float}`
- **Description:** Triggered when a customer places a new order.

## 2. `PAYMENT_PROCESSED`
- **Producer:** `handle_order_created`
- **Payload:** `{"order_id": int, "amount": float}`
- **Description:** Triggered after inventory is reserved and payment is ready to be charged.

## 3. `ORDER_SHIPPED`
- **Producer:** `handle_payment_processed`
- **Payload:** `{"order_id": int}`
- **Description:** Triggered once payment succeeds and the order is dispatched.

## 4. `NOTIFICATION_SENT`
- **Producer:** `handle_order_shipped`
- **Payload:** `{"order_id": int, "message": str}`
- **Description:** Triggered after shipping to notify the customer.
-
