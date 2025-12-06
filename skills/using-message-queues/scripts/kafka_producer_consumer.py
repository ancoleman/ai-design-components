#!/usr/bin/env python3
"""
Kafka Test Utilities
Helper script for testing Kafka producers and consumers
"""
import sys
import argparse
from confluent_kafka import Producer, Consumer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
import json
import uuid
from datetime import datetime


def create_topic(bootstrap_servers: str, topic: str, num_partitions: int = 3, replication_factor: int = 1):
    """Create Kafka topic"""
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    new_topics = [NewTopic(
        topic,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )]

    fs = admin_client.create_topics(new_topics)

    for topic, f in fs.items():
        try:
            f.result()
            print(f"✅ Topic {topic} created")
        except Exception as e:
            print(f"❌ Failed to create topic {topic}: {e}")


def produce_test_messages(bootstrap_servers: str, topic: str, count: int = 10):
    """Produce test messages to topic"""
    producer = Producer({'bootstrap.servers': bootstrap_servers})

    def delivery_callback(err, msg):
        if err:
            print(f'❌ Delivery failed: {err}')
        else:
            print(f'✅ Message {msg.key()} delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}')

    for i in range(count):
        message = {
            'message_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'index': i,
            'data': f'Test message {i}'
        }

        producer.produce(
            topic=topic,
            key=f'key_{i}',
            value=json.dumps(message).encode('utf-8'),
            on_delivery=delivery_callback
        )

    producer.flush()
    print(f"\n✅ Produced {count} messages to {topic}")


def consume_messages(bootstrap_servers: str, topic: str, group_id: str, count: int = 10):
    """Consume messages from topic"""
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([topic])

    messages_consumed = 0

    try:
        while messages_consumed < count:
            msg = consumer.poll(timeout=5.0)

            if msg is None:
                print("⏱️ No more messages")
                break

            if msg.error():
                raise KafkaException(msg.error())

            message = json.loads(msg.value().decode('utf-8'))
            print(f"📨 Received: {message}")
            messages_consumed += 1

    finally:
        consumer.close()

    print(f"\n✅ Consumed {messages_consumed} messages from {topic}")


def list_topics(bootstrap_servers: str):
    """List all Kafka topics"""
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
    metadata = admin_client.list_topics(timeout=10)

    print("\n📋 Topics:")
    for topic in metadata.topics.values():
        print(f"  - {topic.topic} ({len(topic.partitions)} partitions)")


def get_consumer_lag(bootstrap_servers: str, group_id: str):
    """Get consumer group lag"""
    from confluent_kafka.admin import AdminClient

    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    # Get consumer group info
    groups = admin_client.list_consumer_groups()

    print(f"\n📊 Consumer Group: {group_id}")
    # Note: Full lag calculation requires partition assignment info
    print("Use: kafka-consumer-groups --describe --group {group_id} for detailed lag")


def main():
    parser = argparse.ArgumentParser(description='Kafka test utilities')
    parser.add_argument('--bootstrap', default='localhost:9092', help='Kafka bootstrap servers')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Create topic
    create_parser = subparsers.add_parser('create-topic', help='Create topic')
    create_parser.add_argument('topic', help='Topic name')
    create_parser.add_argument('--partitions', type=int, default=3, help='Number of partitions')

    # Produce messages
    produce_parser = subparsers.add_parser('produce', help='Produce test messages')
    produce_parser.add_argument('topic', help='Topic name')
    produce_parser.add_argument('--count', type=int, default=10, help='Number of messages')

    # Consume messages
    consume_parser = subparsers.add_parser('consume', help='Consume messages')
    consume_parser.add_argument('topic', help='Topic name')
    consume_parser.add_argument('--group', default='test-consumer', help='Consumer group ID')
    consume_parser.add_argument('--count', type=int, default=10, help='Number of messages')

    # List topics
    subparsers.add_parser('list', help='List topics')

    args = parser.parse_args()

    if args.command == 'create-topic':
        create_topic(args.bootstrap, args.topic, args.partitions)
    elif args.command == 'produce':
        produce_test_messages(args.bootstrap, args.topic, args.count)
    elif args.command == 'consume':
        consume_messages(args.bootstrap, args.topic, args.group, args.count)
    elif args.command == 'list':
        list_topics(args.bootstrap)


if __name__ == '__main__':
    main()
