"""
Kafka Producer Example
Demonstrates basic and advanced Kafka producer patterns
"""
from confluent_kafka import Producer
import json
import uuid
import time
from datetime import datetime


# Basic Producer Configuration
config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer',
    'acks': 'all',  # Wait for all replicas
    'enable.idempotence': True,  # Prevent duplicates
    'compression.type': 'lz4',  # Fast compression
    'batch.size': 32768,  # 32KB batches
    'linger.ms': 10,  # Wait 10ms for batching
}

producer = Producer(config)


def delivery_callback(err, msg):
    """Callback for message delivery confirmation"""
    if err:
        print(f'❌ Delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')


def produce_simple_message():
    """Example 1: Simple message production"""
    print("\n=== Example 1: Simple Message ===")

    message = {
        'event_type': 'order.created',
        'order_id': 'ord_123',
        'customer_id': 'cus_456',
        'total': 99.99
    }

    producer.produce(
        topic='orders',
        key='ord_123',  # Messages with same key go to same partition
        value=json.dumps(message).encode('utf-8'),
        on_delivery=delivery_callback
    )

    producer.flush()  # Wait for delivery


def produce_with_headers():
    """Example 2: Message with headers (metadata)"""
    print("\n=== Example 2: Message with Headers ===")

    message = {
        'event_type': 'payment.charged',
        'payment_id': 'pay_789',
        'amount': 149.99
    }

    headers = {
        'correlation_id': str(uuid.uuid4()),
        'trace_id': 'trace_123',
        'user_id': 'user_456'
    }

    producer.produce(
        topic='payments',
        key='pay_789',
        value=json.dumps(message).encode('utf-8'),
        headers=headers,
        on_delivery=delivery_callback
    )

    producer.flush()


def produce_batch():
    """Example 3: Batch production for efficiency"""
    print("\n=== Example 3: Batch Production ===")

    start_time = time.time()

    for i in range(100):
        message = {
            'event_type': 'log.message',
            'log_id': f'log_{i}',
            'timestamp': datetime.utcnow().isoformat(),
            'message': f'Log message {i}'
        }

        producer.produce(
            topic='logs',
            key=f'log_{i}',
            value=json.dumps(message).encode('utf-8')
        )

    producer.flush()

    elapsed = time.time() - start_time
    print(f"Produced 100 messages in {elapsed:.2f} seconds ({100/elapsed:.0f} msg/s)")


def produce_with_partitioner():
    """Example 4: Custom partitioning strategy"""
    print("\n=== Example 4: Custom Partitioning ===")

    # VIP customers go to partition 0 for priority processing
    vip_customers = ['cus_vip_1', 'cus_vip_2']
    regular_customers = ['cus_123', 'cus_456', 'cus_789']

    for customer_id in vip_customers + regular_customers:
        message = {
            'event_type': 'order.created',
            'order_id': str(uuid.uuid4()),
            'customer_id': customer_id,
            'total': 99.99
        }

        # Partition based on customer type
        partition = 0 if customer_id.startswith('cus_vip') else -1  # -1 = default partitioner

        producer.produce(
            topic='orders',
            key=customer_id,
            value=json.dumps(message).encode('utf-8'),
            partition=partition if partition >= 0 else None,
            on_delivery=delivery_callback
        )

    producer.flush()


def produce_with_error_handling():
    """Example 5: Robust error handling"""
    print("\n=== Example 5: Error Handling ===")

    def robust_produce(topic, key, value, retries=3):
        """Produce with retry logic"""
        for attempt in range(retries):
            try:
                producer.produce(
                    topic=topic,
                    key=key,
                    value=value,
                    on_delivery=delivery_callback
                )
                producer.flush(timeout=5)
                return True
            except BufferError:
                # Queue full, wait and retry
                print(f"Buffer full, waiting... (attempt {attempt + 1}/{retries})")
                time.sleep(0.1 * (2 ** attempt))
            except Exception as e:
                print(f"Error: {e}")
                if attempt == retries - 1:
                    raise

        return False

    message = {
        'event_type': 'critical.alert',
        'alert_id': str(uuid.uuid4()),
        'severity': 'high'
    }

    robust_produce(
        topic='alerts',
        key='alert_123',
        value=json.dumps(message).encode('utf-8')
    )


if __name__ == "__main__":
    print("🚀 Kafka Producer Examples")
    print("=" * 50)

    try:
        produce_simple_message()
        produce_with_headers()
        produce_batch()
        produce_with_partitioner()
        produce_with_error_handling()

        print("\n✅ All examples completed successfully")

    finally:
        producer.flush()
        print("\n👋 Producer shut down")
