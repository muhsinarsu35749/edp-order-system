# System Architecture

This application follows a local Event-Driven Architecture (EDA) using an in-memory FIFO event queue.

## Components

### 1. Event Producers
Components that generate events and push them into the queue using `publish()`:
- **Order Entry:** Produces initial `ORDER_CREATED` events.
- **Event Handlers:** Act as secondary producers by emitting the next event in the workflow (`PAYMENT_PROCESSED`, `ORDER_SHIPPED`, `NOTIFICATION_SENT`).

### 2. Event Queue
- Implemented locally using Python's `collections.deque`.
- Stores events in FIFO (First-In, First-Out) order until the event loop consumes them.

### 3. Event Loop & Dispatcher
- Continuously polls `event_queue` while it is not empty.
- Pops the oldest event and routes it to all subscribed handlers in the `handlers` registry.

### 4. Event Handlers (Consumers)
Functions subscribed to specific event types via `subscribe()`:
- `handle_order_created`: Reserves stock and emits `PAYMENT_PROCESSED`.
- `handle_payment_processed`: Processes payment and emits `ORDER_SHIPPED`.
- `handle_order_shipped`: Dispatches the package and emits `NOTIFICATION_SENT`.
- `handle_notification_sent`: Sends the final confirmation message to the user.

## Architecture Flow

```text
+-----------------+       publish()       +-------------------+
| Event Producers | --------------------> | Local Event Queue |
+-----------------+                       |     (deque)       |
        ^                                 +-------------------+
        |                                           |
        | emits next event                          | popleft()
        |                                           v
+-----------------+      dispatches       +-------------------+
| Event Handlers  | <-------------------- |    Event Loop     |
+-----------------+                       +-------------------+
