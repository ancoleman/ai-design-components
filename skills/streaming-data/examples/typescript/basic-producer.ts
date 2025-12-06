/**
 * Basic Kafka Producer Example (TypeScript/KafkaJS)
 *
 * Demonstrates:
 * - Producer configuration with at-least-once delivery
 * - Sending messages with keys and headers
 * - Error handling with delivery callbacks
 * - Graceful shutdown
 *
 * Dependencies:
 *   npm install kafkajs
 *
 * Usage:
 *   npx ts-node basic-producer.ts
 */

import { Kafka, CompressionTypes, Partitioners, RecordMetadata } from 'kafkajs';

interface UserEvent {
  userId: string;
  action: string;
  timestamp: number;
}

class BasicProducer {
  private kafka: Kafka;
  private producer: any;

  constructor(brokers: string[]) {
    this.kafka = new Kafka({
      clientId: 'basic-producer-example',
      brokers: brokers,
    });

    this.producer = this.kafka.producer({
      createPartitioner: Partitioners.LegacyPartitioner,
      // At-least-once delivery guarantees
      idempotent: true,
      maxInFlightRequests: 5,
    });
  }

  async connect(): Promise<void> {
    await this.producer.connect();
    console.log('✓ Producer connected');
  }

  async sendEvent(topic: string, event: UserEvent): Promise<void> {
    try {
      const metadata: RecordMetadata[] = await this.producer.send({
        topic,
        compression: CompressionTypes.GZIP,
        messages: [
          {
            key: event.userId,
            value: JSON.stringify(event),
            headers: {
              'event-type': event.action,
              'timestamp': event.timestamp.toString(),
            },
          },
        ],
      });

      console.log(`✓ Event sent to partition ${metadata[0].partition}, offset ${metadata[0].offset}`);
    } catch (error) {
      console.error('✗ Failed to send event:', error);
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    await this.producer.disconnect();
    console.log('✓ Producer disconnected');
  }
}

// Main execution
async function main() {
  const producer = new BasicProducer(['localhost:9092']);

  try {
    await producer.connect();

    // Send some example events
    for (let i = 0; i < 10; i++) {
      await producer.sendEvent('user-actions', {
        userId: `user-${i}`,
        action: 'login',
        timestamp: Date.now(),
      });
    }

    console.log('✓ All events sent successfully');
  } catch (error) {
    console.error('✗ Error:', error);
    process.exit(1);
  } finally {
    await producer.disconnect();
  }
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { BasicProducer, UserEvent };
