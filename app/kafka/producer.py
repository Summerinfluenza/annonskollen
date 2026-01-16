import json
from kafka import KafkaProducer
from app.core.logger import get_logger

logger = get_logger("KafkaProducer")

class MessageProducer:
    def __init__(self, broker="localhost:9092"):
        self.producer = KafkaProducer(
            bootstrap_servers=broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_resume_event(self, user_id, resume_text):
        try:
            payload = {"user_id": user_id, "resume": resume_text}
            self.producer.send("resume_uploaded", payload)
            logger.info(f"Sent resume_uploaded event for user: {user_id}")
        except Exception as e:
            logger.error(f"Failed to send Kafka message: {e}")