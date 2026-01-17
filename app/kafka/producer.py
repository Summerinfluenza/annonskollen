import json
from kafka import KafkaProducer
from app.core.logger import get_logger

logger = get_logger("KafkaProducer")

class MessageProducer:
    def __init__(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers="localhost:9092",
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=5000
            )
            logger.info("Kafka Producer initialized successfully")
        except Exception as e:
            logger.error(f"KAFKA ERROR: Could not connect to broker: {e}")
            self.producer = None

    def send_resume_event(self, user_id, resume_text):
        try:
            payload = {"user_id": user_id, "resume": resume_text}
            self.producer.send("resume_uploaded", payload)
            logger.info(f"Sent resume_uploaded event for user: {user_id}")
        except Exception as e:
            logger.error(f"Failed to send Kafka message: {e}")
    
    def send_fetch_job_event(self, user_id, municipality):
        try:
            payload = {"user_id": user_id, "municipality": municipality}
            self.producer.send("fetch_job", payload)
            logger.info(f"Sent fetch_job event for user: {user_id}")
        except Exception as e:
            logger.error(f"Failed to send Kafka message: {e}")
    
    def send_match_job_event(self, user_id):
        try:
            payload = {"user_id": user_id}
            self.producer.send("match_job", payload)
            self.producer.flush()
            logger.info(f"Sent match_job event for user: {user_id}")
        except Exception as e:
            logger.error(f"Failed to send Kafka message: {e}")