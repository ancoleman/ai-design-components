"""
Temporal Workflow for Order Processing Saga
Demonstrates distributed transactions with compensation
"""
from temporalio import workflow
from datetime import timedelta
from typing import Optional
import logging


@workflow.defn
class OrderSagaWorkflow:
    """
    Order processing workflow with saga pattern

    Steps:
    1. Reserve inventory
    2. Charge payment
    3. Ship order
    4. Send confirmation

    If any step fails, compensate in reverse order
    """

    def __init__(self):
        self.logger = workflow.logger

    @workflow.run
    async def run(self, order_id: str, customer_id: str, items: list, total: float) -> dict:
        """
        Execute order processing saga

        Args:
            order_id: Unique order identifier
            customer_id: Customer ID
            items: List of items (dict with item_id, quantity, price)
            total: Total order amount

        Returns:
            Result dictionary with status and details
        """
        self.logger.info(f"Starting order saga for {order_id}")

        # Track resources for compensation
        reservation_id: Optional[str] = None
        payment_id: Optional[str] = None
        shipment_id: Optional[str] = None

        try:
            # Step 1: Reserve inventory
            self.logger.info(f"Step 1: Reserving inventory for {order_id}")
            reservation_id = await workflow.execute_activity(
                "reserve_inventory",
                args=[order_id, items],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=workflow.RetryPolicy(
                    maximum_attempts=3,
                    backoff_coefficient=2.0,
                )
            )
            self.logger.info(f"Inventory reserved: {reservation_id}")

            # Step 2: Charge payment
            self.logger.info(f"Step 2: Charging payment for {order_id}")
            payment_id = await workflow.execute_activity(
                "charge_payment",
                args=[order_id, customer_id, total],
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=workflow.RetryPolicy(
                    maximum_attempts=3,
                    backoff_coefficient=2.0,
                )
            )
            self.logger.info(f"Payment charged: {payment_id}")

            # Step 3: Ship order
            self.logger.info(f"Step 3: Shipping order {order_id}")
            shipment_id = await workflow.execute_activity(
                "ship_order",
                args=[order_id, customer_id, items],
                start_to_close_timeout=timedelta(minutes=10),
                retry_policy=workflow.RetryPolicy(
                    maximum_attempts=3,
                    backoff_coefficient=2.0,
                )
            )
            self.logger.info(f"Order shipped: {shipment_id}")

            # Step 4: Send confirmation email
            self.logger.info(f"Step 4: Sending confirmation for {order_id}")
            await workflow.execute_activity(
                "send_confirmation_email",
                args=[order_id, customer_id, shipment_id],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=workflow.RetryPolicy(
                    maximum_attempts=5,
                    backoff_coefficient=1.5,
                )
            )

            self.logger.info(f"✅ Order {order_id} completed successfully")

            return {
                "status": "success",
                "order_id": order_id,
                "reservation_id": reservation_id,
                "payment_id": payment_id,
                "shipment_id": shipment_id
            }

        except Exception as e:
            self.logger.error(f"❌ Order {order_id} failed: {str(e)}")

            # COMPENSATION LOGIC (rollback in reverse order)
            try:
                # Compensate: Cancel shipment (if created)
                if shipment_id:
                    self.logger.info(f"Compensation: Canceling shipment {shipment_id}")
                    await workflow.execute_activity(
                        "cancel_shipment",
                        shipment_id,
                        start_to_close_timeout=timedelta(seconds=60),
                    )

                # Compensate: Refund payment (if charged)
                if payment_id:
                    self.logger.info(f"Compensation: Refunding payment {payment_id}")
                    await workflow.execute_activity(
                        "refund_payment",
                        payment_id,
                        start_to_close_timeout=timedelta(seconds=60),
                    )

                # Compensate: Release inventory (if reserved)
                if reservation_id:
                    self.logger.info(f"Compensation: Releasing inventory {reservation_id}")
                    await workflow.execute_activity(
                        "release_inventory",
                        reservation_id,
                        start_to_close_timeout=timedelta(seconds=30),
                    )

                # Notify customer of failure
                await workflow.execute_activity(
                    "send_failure_notification",
                    args=[order_id, customer_id, str(e)],
                    start_to_close_timeout=timedelta(seconds=30),
                )

            except Exception as comp_error:
                self.logger.error(f"⚠️ Compensation failed: {str(comp_error)}")

            return {
                "status": "failed",
                "order_id": order_id,
                "error": str(e),
                "compensated": True
            }


@workflow.defn
class OrderWithApprovalWorkflow:
    """
    Order processing with human approval step

    Use case: High-value orders requiring manual approval
    """

    def __init__(self):
        self.approved = False
        self.rejected = False
        self.approval_notes = ""

    @workflow.run
    async def run(self, order_id: str, customer_id: str, total: float) -> dict:
        """Execute order with approval gate"""

        # Validate order
        await workflow.execute_activity(
            "validate_order",
            args=[order_id, customer_id, total],
            start_to_close_timeout=timedelta(seconds=10),
        )

        # If high value, require approval
        if total > 1000:
            workflow.logger.info(f"Order {order_id} requires approval (${total})")

            # Notify approver
            await workflow.execute_activity(
                "notify_approver",
                args=[order_id, total],
                start_to_close_timeout=timedelta(seconds=10),
            )

            # Wait for approval (up to 24 hours)
            approved = await workflow.wait_condition(
                lambda: self.approved or self.rejected,
                timeout=timedelta(hours=24)
            )

            if not approved:
                # Timeout
                workflow.logger.warning(f"Order {order_id} approval timeout")
                return {"status": "timeout", "order_id": order_id}

            if self.rejected:
                workflow.logger.info(f"Order {order_id} rejected: {self.approval_notes}")
                await workflow.execute_activity(
                    "send_rejection_email",
                    args=[order_id, customer_id, self.approval_notes],
                    start_to_close_timeout=timedelta(seconds=30),
                )
                return {
                    "status": "rejected",
                    "order_id": order_id,
                    "notes": self.approval_notes
                }

        # Process approved order (delegate to saga workflow)
        result = await workflow.execute_child_workflow(
            OrderSagaWorkflow.run,
            args=[order_id, customer_id, [], total],
            id=f"order-saga-{order_id}",
        )

        return result

    @workflow.signal
    def approve(self, notes: str = ""):
        """Signal: Approve order"""
        workflow.logger.info(f"Order approved: {notes}")
        self.approved = True
        self.approval_notes = notes

    @workflow.signal
    def reject(self, notes: str):
        """Signal: Reject order"""
        workflow.logger.info(f"Order rejected: {notes}")
        self.rejected = True
        self.approval_notes = notes

    @workflow.query
    def get_status(self) -> dict:
        """Query: Get approval status"""
        return {
            "approved": self.approved,
            "rejected": self.rejected,
            "pending": not (self.approved or self.rejected),
            "notes": self.approval_notes
        }
