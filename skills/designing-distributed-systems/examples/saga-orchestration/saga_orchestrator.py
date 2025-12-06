"""
Saga Orchestration Pattern

Demonstrates: Saga orchestrator with compensating transactions

Dependencies:
    - Python 3.7+

Usage:
    python saga_orchestrator.py
"""

class SagaOrchestrator:
    """Orchestrator for distributed transactions with compensation"""

    def __init__(self):
        self.steps = []
        self.compensations = []

    def add_step(self, name, action, compensation):
        """Add saga step with compensating action"""
        self.steps.append({'name': name, 'action': action})
        self.compensations.append({'name': name, 'compensation': compensation})

    def execute(self, context):
        """Execute saga with automatic rollback on failure"""
        executed_steps = []

        print(f"Starting saga with context: {context}\n")

        try:
            for step in self.steps:
                print(f"Executing: {step['name']}")
                result = step['action'](context)
                executed_steps.append(step)
                context.update(result)
                print(f"  Success: {result}\n")

            print(f"Saga completed successfully!")
            return {'status': 'success', 'context': context}

        except Exception as e:
            print(f"  Failed: {e}\n")
            print(f"Rolling back {len(executed_steps)} executed steps...")

            # Rollback in reverse order
            for step in reversed(executed_steps):
                idx = self.steps.index(step)
                compensation = self.compensations[idx]
                try:
                    print(f"Compensating: {compensation['name']}")
                    compensation['compensation'](context)
                    print(f"  Compensated\n")
                except Exception as comp_error:
                    print(f"  Compensation failed: {comp_error}\n")

            return {'status': 'failed', 'error': str(e)}


# Mock services
class OrderService:
    def create_order(self, context):
        order_id = f"order-{context['product_id']}"
        print(f"  Creating order {order_id}")
        return {'order_id': order_id, 'status': 'created'}

    def cancel_order(self, context):
        print(f"  Cancelling order {context['order_id']}")

class PaymentService:
    def process_payment(self, context):
        payment_id = f"payment-{context['order_id']}"
        if context.get('fail_payment'):
            raise Exception("Payment declined")
        print(f"  Processing payment {payment_id}")
        return {'payment_id': payment_id}

    def refund(self, context):
        print(f"  Refunding payment {context['payment_id']}")

class InventoryService:
    def reserve(self, context):
        reservation_id = f"reservation-{context['product_id']}"
        print(f"  Reserving inventory {reservation_id}")
        return {'reservation_id': reservation_id}

    def release(self, context):
        print(f"  Releasing inventory {context.get('reservation_id', 'N/A')}")


if __name__ == "__main__":
    order_service = OrderService()
    payment_service = PaymentService()
    inventory_service = InventoryService()

    # Create saga
    saga = SagaOrchestrator()

    saga.add_step(
        name="Create Order",
        action=order_service.create_order,
        compensation=order_service.cancel_order
    )

    saga.add_step(
        name="Process Payment",
        action=payment_service.process_payment,
        compensation=payment_service.refund
    )

    saga.add_step(
        name="Reserve Inventory",
        action=inventory_service.reserve,
        compensation=inventory_service.release
    )

    # Scenario 1: Success
    print("Scenario 1: All steps succeed")
    print("=" * 60)
    result = saga.execute({'product_id': 'prod-123'})
    print(f"Result: {result['status']}\n\n")

    # Scenario 2: Payment failure
    print("Scenario 2: Payment fails, trigger compensation")
    print("=" * 60)
    result = saga.execute({'product_id': 'prod-456', 'fail_payment': True})
    print(f"Result: {result['status']}")
