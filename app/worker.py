import json
from kafka import KafkaConsumer
from app.services.ai_engine import AIEngine
from app.services.job_manager import JobManager
from app.db.firebase_admin import initialize_db
from app.core.logger import get_logger

logger = get_logger("Worker")

class Worker:
    def __init__(self):
        self.db = initialize_db()
        self.ai = AIEngine(db_instance=self.db)
        self.job_manager = JobManager(db_instance=self.db)
        
        self.consumer = KafkaConsumer(
            "resume_uploaded", "fetch_job", "match_job",
            bootstrap_servers="localhost:9092",
            group_id="job_processor_v1",
            auto_offset_reset='earliest', 
            enable_auto_commit=True, 
            heartbeat_interval_ms=3000, 
            session_timeout_ms=10000,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def handle_resume_upload(self, data):
        user_id = data.get("user_id")
        resume = data.get("resume")
        
        logger.info(f"Task: Extracting tags for user {user_id}")
        self.ai.extract_resume_tags(user_id, resume)

    def handle_fetch_job(self, data):
        user_id = data.get("user_id")
        municipality = data.get("municipality")
        
        logger.info(f"Task: Fetching initial jobs for {user_id}")
        self.job_manager.fetch_and_store_jobs(user_id, municipality)

    def handle_match_job(self, data):
        user_id = data.get("user_id")

        logger.info(f"Task: Matching initial jobs for {user_id}")
        self.job_manager.match_jobs_with_ai(user_id)

    def run(self):
        logger.info("Worker started. Listening for messages...")
        for message in self.consumer:
            topic = message.topic
            data = message.value
            logger.debug(f"Received message from {topic}")
            
            try:
                if topic == "resume_uploaded":
                    self.handle_resume_upload(data)
                elif topic == "fetch_job":
                    self.handle_fetch_job(data)
                elif topic == "match_job":
                    self.handle_match_job(data)
                logger.info(f"Successfully completed task from topic: {topic}")
            except Exception as e:
                logger.error(f"Failed to process message from {topic}: {e}")

if __name__ == "__main__":
    worker = Worker()
    worker.run()