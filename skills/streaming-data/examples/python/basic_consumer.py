"""
Basic Kafka Consumer Example (Python/confluent-kafka-python)

Demonstrates:
- Consumer configuration with manual offset commits
- Processing messages with error handling
- Dead-letter queue pattern
- Graceful shutdown

Dependencies:
    pip install confluent-kafka

Usage:
    python basic_consumer.py
"""

from confluent_kafka import Consumer, Producer, KafkaException
import json
import signal
import sys

class BasicConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        """Initialize Kafka consumer with manual offset management."""
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            # Manual commit for error handling
            'enable.auto.commit': False,
        }
        self.consumer = Consumer(self.config)
        self.running = True

        # DLQ producer
        self.dlq_producer = Producer({
            'bootstrap.servers': bootstrap_servers,
        })

    def subscribe(self, topics: list):
        """Subscribe to topics."""
        self.consumer.subscribe(topics)
        print(f'✓ Subscribed to topics: {topics}')

    def consume(self, handler):
        """Start consuming messages."""
        print('✓ Consumer started, waiting for messages...')

        try:
            while self.running:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    raise KafkaException(msg.error())

                try:
                    # Decode message
                    value = json.loads(msg.value().decode('utf-8'))

                    # Process message
                    handler(value)

                    # Commit offset after successful processing
                    self.consumer.commit(message=msg)
                    print(f'✓ Processed and committed offset {msg.offset()}')

                except json.JSONDecodeError as e:
                    print(f'✗ Failed to decode message: {e}')
                    self._send_to_dlq(msg, str(e))
                    self.consumer.commit(message=msg)

                except Exception as e:
                    print(f'✗ Error processing message: {e}')
                    # Don't commit - message will be reprocessed

        except KeyboardInterrupt:
            print('\\n✓ Shutdown signal received')
        finally:
            self.close()

    def _send_to_dlq(self, msg, error: str):
        """Send failed message to dead-letter queue."""
        dlq_topic = f'{msg.topic()}.dlq'

        self.dlq_producer.produce(
            topic=dlq_topic,
            key=msg.key(),
            value=msg.value(),
            headers={
                'original-topic': msg.topic(),
                'error-message': error,
            }
        )
        self.dlq_producer.flush()
        print(f'✓ Sent message to DLQ: {dlq_topic}')

    def close(self):
        """Close the consumer."""
        self.consumer.close()
        self.dlq_producer.flush()
        print('✓ Consumer closed')

    def shutdown(self, signum, frame):
        """Graceful shutdown handler."""
        print('\\n✓ Shutting down gracefully...')
        self.running = False

def handle_event(event: dict):
    """Example event handler."""
    print(f'Processing event: {event}')
    # Your business logic here

if __name__ == '__main__':
    consumer = BasicConsumer('localhost:9092', 'basic-consumer-group')

    # Set up signal handlers
    signal.signal(signal.SIGINT, consumer.shutdown)
    signal.signal(signal.SIGTERM, consumer.shutdown)

    consumer.subscribe(['user-actions'])
    consumer.consume(handle_event)
