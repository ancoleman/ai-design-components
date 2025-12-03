"""
Temporal Activities for Order Processing
Activities represent external side effects (API calls, database writes)
"""
from temporalio import activity
import asyncio
import random
import logging


# Configure logger
logger = logging.getLogger(__name__)


@activity.defn
async def reserve_inventory(order_id: str, items: list) -> str:
    """
    Reserve inventory for order

    Args:
        order_id: Order ID
        items: List of items to reserve

    Returns:
        Reservation ID

    Raises:
        ValueError: Insufficient stock
    """
    logger.info(f"Reserving inventory for order {order_id}")
    activity.heartbeat()  # Send heartbeat to Temporal

    # Simulate API call to inventory service
    await asyncio.sleep(0.5)

    # Simulate occasional failures (10% chance)
    if random.random() < 0.1:
        raise Exception("Inventory service unavailable")

    # Check stock
    for item in items:
        available = random.randint(0, 100)
        if available < item['quantity']:
            raise ValueError(f"Insufficient stock for {item['item_id']}")

    reservation_id = f"rsv_{order_id}"
    logger.info(f"✅ Inventory reserved: {reservation_id}")
    return reservation_id


@activity.defn
async def release_inventory(reservation_id: str) -> None:
    """
    Release inventory reservation (compensation)

    Args:
        reservation_id: Reservation to release
    """
    logger.info(f"Releasing inventory reservation {reservation_id}")
    await asyncio.sleep(0.3)
    logger.info(f"✅ Inventory released: {reservation_id}")


@activity.defn
async def charge_payment(order_id: str, customer_id: str, amount: float) -> str:
    """
    Charge payment for order

    Args:
        order_id: Order ID
        customer_id: Customer ID
        amount: Amount to charge

    Returns:
        Payment ID

    Raises:
        ValueError: Payment declined
    """
    logger.info(f"Charging ${amount} for order {order_id}")
    activity.heartbeat()

    # Simulate payment gateway call
    await asyncio.sleep(1.0)

    # Simulate payment failures (5% chance)
    if random.random() < 0.05:
        raise ValueError("Payment declined")

    payment_id = f"pay_{order_id}"
    logger.info(f"✅ Payment charged: {payment_id}")
    return payment_id


@activity.defn
async def refund_payment(payment_id: str) -> None:
    """
    Refund payment (compensation)

    Args:
        payment_id: Payment to refund
    """
    logger.info(f"Refunding payment {payment_id}")
    await asyncio.sleep(0.8)
    logger.info(f"✅ Payment refunded: {payment_id}")


@activity.defn
async def ship_order(order_id: str, customer_id: str, items: list) -> str:
    """
    Ship order to customer

    Args:
        order_id: Order ID
        customer_id: Customer ID
        items: Items to ship

    Returns:
        Shipment tracking number

    Raises:
        Exception: Shipping service errors
    """
    logger.info(f"Shipping order {order_id}")
    activity.heartbeat()

    # Simulate shipping service call
    await asyncio.sleep(2.0)

    # Simulate occasional failures
    if random.random() < 0.03:
        raise Exception("Shipping service unavailable")

    shipment_id = f"ship_{order_id}"
    logger.info(f"✅ Order shipped: {shipment_id}")
    return shipment_id


@activity.defn
async def cancel_shipment(shipment_id: str) -> None:
    """
    Cancel shipment (compensation)

    Args:
        shipment_id: Shipment to cancel
    """
    logger.info(f"Canceling shipment {shipment_id}")
    await asyncio.sleep(0.5)
    logger.info(f"✅ Shipment canceled: {shipment_id}")


@activity.defn
async def send_confirmation_email(order_id: str, customer_id: str, shipment_id: str) -> None:
    """
    Send order confirmation email

    Args:
        order_id: Order ID
        customer_id: Customer ID
        shipment_id: Shipment tracking number
    """
    logger.info(f"Sending confirmation email for order {order_id}")
    await asyncio.sleep(0.3)
    logger.info(f"✅ Confirmation email sent to {customer_id}")


@activity.defn
async def send_failure_notification(order_id: str, customer_id: str, error: str) -> None:
    """
    Notify customer of order failure

    Args:
        order_id: Order ID
        customer_id: Customer ID
        error: Error message
    """
    logger.info(f"Sending failure notification for order {order_id}")
    await asyncio.sleep(0.3)
    logger.info(f"✅ Failure notification sent to {customer_id}")


@activity.defn
async def validate_order(order_id: str, customer_id: str, total: float) -> None:
    """
    Validate order details

    Args:
        order_id: Order ID
        customer_id: Customer ID
        total: Order total

    Raises:
        ValueError: Invalid order
    """
    logger.info(f"Validating order {order_id}")
    await asyncio.sleep(0.2)

    if total <= 0:
        raise ValueError("Invalid order total")

    logger.info(f"✅ Order validated: {order_id}")


@activity.defn
async def notify_approver(order_id: str, total: float) -> None:
    """
    Notify approver of order requiring approval

    Args:
        order_id: Order ID
        total: Order total
    """
    logger.info(f"Notifying approver for order {order_id} (${total})")
    await asyncio.sleep(0.3)
    logger.info(f"✅ Approver notified for order {order_id}")


@activity.defn
async def send_rejection_email(order_id: str, customer_id: str, notes: str) -> None:
    """
    Send order rejection email

    Args:
        order_id: Order ID
        customer_id: Customer ID
        notes: Rejection notes
    """
    logger.info(f"Sending rejection email for order {order_id}")
    await asyncio.sleep(0.3)
    logger.info(f"✅ Rejection email sent to {customer_id}")
