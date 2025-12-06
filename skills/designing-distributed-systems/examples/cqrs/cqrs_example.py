"""
CQRS (Command Query Responsibility Segregation) Pattern

Demonstrates: Separate read/write models

Dependencies:
    - Python 3.7+

Usage:
    python cqrs_example.py
"""

from datetime import datetime
from typing import Dict, List

# Write Model (Command Side)
class OrderWriteModel:
    """Normalized write model for commands"""

    def __init__(self):
        self.orders = {}  # order_id -> order
        self.order_items = {}  # order_id -> [items]
        self.event_handlers = []

    def create_order(self, command: Dict):
        """Handle CreateOrder command"""
        order_id = command['order_id']

        if order_id in self.orders:
            raise ValueError(f"Order {order_id} already exists")

        # Write to normalized storage
        self.orders[order_id] = {
            'order_id': order_id,
            'customer_id': command['customer_id'],
            'status': 'pending',
            'created_at': datetime.utcnow()
        }

        self.order_items[order_id] = command['items']

        # Publish event for read model update
        event = {
            'type': 'OrderCreated',
            'order_id': order_id,
            'customer_id': command['customer_id'],
            'items': command['items'],
            'timestamp': datetime.utcnow()
        }

        for handler in self.event_handlers:
            handler(event)

        print(f"[Write Model] Created order {order_id}")
        return order_id

    def add_event_handler(self, handler):
        """Register event handler"""
        self.event_handlers.append(handler)


# Read Model (Query Side)
class OrderReadModel:
    """Denormalized read model for queries"""

    def __init__(self):
        self.orders_cache = {}  # order_id -> denormalized order
        self.customer_orders_index = {}  # customer_id -> [order_ids]

    def get_order(self, order_id: str) -> Dict:
        """Get order summary (optimized read)"""
        return self.orders_cache.get(order_id)

    def get_customer_orders(self, customer_id: str) -> List[Dict]:
        """Get all orders for customer"""
        order_ids = self.customer_orders_index.get(customer_id, [])
        return [self.orders_cache[oid] for oid in order_ids if oid in self.orders_cache]

    def update_from_event(self, event):
        """Update read model from event"""
        if event['type'] == 'OrderCreated':
            order_id = event['order_id']
            customer_id = event['customer_id']

            # Denormalized document (optimized for reads)
            order_doc = {
                'order_id': order_id,
                'customer_id': customer_id,
                'items': event['items'],
                'item_count': len(event['items']),
                'total_quantity': sum(item['quantity'] for item in event['items']),
                'created_at': event['timestamp'],
                'status': 'pending'
            }

            # Update cache
            self.orders_cache[order_id] = order_doc

            # Update customer index
            if customer_id not in self.customer_orders_index:
                self.customer_orders_index[customer_id] = []
            self.customer_orders_index[customer_id].append(order_id)

            print(f"[Read Model] Updated order {order_id} in cache and indexes")


if __name__ == "__main__":
    print("CQRS Pattern Demo\n")

    # Create write and read models
    write_model = OrderWriteModel()
    read_model = OrderReadModel()

    # Connect event handler
    write_model.add_event_handler(read_model.update_from_event)

    # Command: Create order
    print("Command: Create Order")
    print("=" * 60)
    command = {
        'order_id': 'order-123',
        'customer_id': 'customer-456',
        'items': [
            {'product_id': 'prod-1', 'quantity': 2, 'price': 50},
            {'product_id': 'prod-2', 'quantity': 1, 'price': 100}
        ]
    }
    write_model.create_order(command)

    # Query: Get order (from read model)
    print("\nQuery: Get Order")
    print("=" * 60)
    order = read_model.get_order('order-123')
    print(f"Order summary: {order}")

    # Create another order for same customer
    print("\nCommand: Create Another Order")
    print("=" * 60)
    command2 = {
        'order_id': 'order-124',
        'customer_id': 'customer-456',
        'items': [
            {'product_id': 'prod-3', 'quantity': 1, 'price': 200}
        ]
    }
    write_model.create_order(command2)

    # Query: Get customer orders
    print("\nQuery: Get Customer Orders")
    print("=" * 60)
    customer_orders = read_model.get_customer_orders('customer-456')
    print(f"Customer has {len(customer_orders)} orders:")
    for order in customer_orders:
        print(f"  - {order['order_id']}: {order['item_count']} items, "
              f"{order['total_quantity']} total quantity")
