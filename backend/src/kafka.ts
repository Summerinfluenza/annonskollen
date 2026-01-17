import { Kafka } from 'kafkajs';
import { logger } from './logger';

const kafka = new Kafka({
  clientId: 'annonskollen-backend',
  brokers: ['localhost:9092'], 
});

const producer = kafka.producer();

export const initKafka = async () => {
  try {
    await producer.connect();
    logger.info('Kafka Producer connected');
  } catch (error) {
    logger.error(error, 'Kafka connection failed');
  }
};

export const produceEvent = async (topic: string, payload: object) => {
  try {
    await producer.send({
      topic,
      messages: [{ value: JSON.stringify(payload) }],
    });
    logger.info({ topic }, 'Message sent to Kafka');
  } catch (error) {
    logger.error({ error, topic }, 'Failed to send Kafka message');
  }
};