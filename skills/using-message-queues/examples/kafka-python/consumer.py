"""
Kafka Consumer Example
Demonstrates consumer groups, manual commits, and error handling
"""
from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import time


# Consumer Configuration
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest',  # Start from beginning if no offset
    'enable.auto.commit': False,  # Manual commit for exactly-once
    'max.poll.interval.ms': 300000,  # 5 minutes max processing time
    'session.timeout.ms': 30000,  # 30 seconds
}

consumer = Consumer(config)


def consume_with_manual_commit():
    """Example 1: Manual commit after processing"""
    print("\n=== Example 1: Manual Commit ===")

    consumer.subscribe(['orders'])

    try:
        for _ in range(10):  # Process 10 messages
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f'End of partition {msg.partition()}')
                else:
                    raise KafkaException(msg.error())
            else:
                # Process message
                try:
                    order = json.loads(msg.value().decode('utf-8'))
                    print(f'📦 Processing order: {order.get("order_id")}')

                    # Simulate processing
                    time.sleep(0.1)

                    # Commit after successful processing
                    consumer.commit(message=msg)
                    print(f'✅ Committed offset {msg.offset()}')

                except json.JSONDecodeError as e:
                    print(f'❌ Invalid JSON: {e}')
                    # Don't commit - message will be redelivered
                except Exception as e:
                    print(f'❌ Processing failed: {e}')
                    # Decide: commit (skip message) or don't commit (retry)

    finally:
        consumer.close()


def consume_with_batching():
    """Example 2: Batch processing for efficiency"""
    print("\n=== Example 2: Batch Processing ===")

    consumer.subscribe(['logs'])

    batch = []
    batch_size = 10

    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                if batch:
                    # Process partial batch on timeout
                    process_batch(batch)
                    consumer.commit()
                    batch = []
                continue

            if msg.error():
                continue

            # Add to batch
            log = json.loads(msg.value().decode('utf-8'))
            batch.append(log)

            if len(batch) >= batch_size:
                # Process full batch
                process_batch(batch)
                consumer.commit()
                batch = []

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        consumer.close()


def process_batch(batch):
    """Process batch of messages"""
    print(f'📊 Processing batch of {len(batch)} messages')
    # Bulk insert to database, send to analytics, etc.
    time.sleep(0.1)


def consume_with_error_handling():
    """Example 3: Robust error handling"""
    print("\n=== Example 3: Error Handling ===")

    consumer.subscribe(['payments'])

    def process_payment(payment_data):
        """Process payment with error handling"""
        payment_id = payment_data.get('payment_id')

        if payment_data.get('amount', 0) <= 0:
            raise ValueError(f"Invalid amount for {payment_id}")

        # Simulate processing
        print(f'💳 Processing payment: {payment_id}')
        time.sleep(0.1)

    try:
        for _ in range(10):
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                continue

            try:
                payment = json.loads(msg.value().decode('utf-8'))
                process_payment(payment)
                consumer.commit(message=msg)

            except ValueError as e:
                # Unrecoverable error - skip message
                print(f'❌ Unrecoverable error: {e}')
                # Send to DLQ
                send_to_dlq(msg)
                consumer.commit(message=msg)  # Don't reprocess

            except Exception as e:
                # Recoverable error - don't commit (will retry)
                print(f'⚠️ Recoverable error: {e}')
                # Message will be redelivered

    finally:
        consumer.close()


def send_to_dlq(msg):
    """Send failed message to dead letter queue"""
    print(f'📬 Sending to DLQ: {msg.key()}')
    # Implement DLQ logic here


def consume_multiple_topics():
    """Example 4: Subscribe to multiple topics"""
    print("\n=== Example 4: Multiple Topics ===")

    consumer.subscribe(['orders', 'payments', 'inventory'])

    try:
        for _ in range(10):
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                continue

            topic = msg.topic()
            data = json.loads(msg.value().decode('utf-8'))

            # Route based on topic
            if topic == 'orders':
                process_order(data)
            elif topic == 'payments':
                process_payment(data)
            elif topic == 'inventory':
                process_inventory(data)

            consumer.commit(message=msg)

    finally:
        consumer.close()


def process_order(data):
    print(f'📦 Order: {data.get("order_id")}')


def process_inventory(data):
    print(f'📊 Inventory: {data.get("item_id")}')


def consume_with_offset_management():
    """Example 5: Manual offset management"""
    print("\n=== Example 5: Manual Offset Management ===")

    from confluent_kafka import TopicPartition

    consumer.subscribe(['orders'])

    try:
        # Wait for partition assignment
        while not consumer.assignment():
            consumer.poll(timeout=1.0)

        # Get assigned partitions
        partitions = consumer.assignment()
        print(f'Assigned partitions: {[p.partition for p in partitions]}')

        # Get committed offsets
        committed = consumer.committed(partitions)
        for partition in committed:
            print(f'Partition {partition.partition}: offset {partition.offset}')

        # Seek to specific offset (e.g., replay from 10 messages ago)
        for partition in partitions:
            current_offset = consumer.committed([partition])[0].offset
            new_offset = max(0, current_offset - 10)
            consumer.seek(TopicPartition(partition.topic, partition.partition, new_offset))

        # Consume from new offset
        for _ in range(10):
            msg = consumer.poll(timeout=1.0)
            if msg and not msg.error():
                print(f'Message offset: {msg.offset()}')
                consumer.commit(message=msg)

    finally:
        consumer.close()


if __name__ == "__main__":
    print("🚀 Kafka Consumer Examples")
    print("=" * 50)

    try:
        # Run examples (uncomment as needed)
        consume_with_manual_commit()
        # consume_with_batching()
        # consume_with_error_handling()
        # consume_multiple_topics()
        # consume_with_offset_management()

        print("\n✅ All examples completed successfully")

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    finally:
        consumer.close()
        print("\n👋 Consumer shut down")
