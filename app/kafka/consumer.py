from kafka import KafkaConsumer
import json
from app.services.ai_engine import AIEngine
from app.services.job_manager import JobManager
from app.db.firebase_admin import get_db
from app.core.logger import get_logger

logger = get_logger("Worker")

# Initialize Services
db = get_db()
ai_engine = AIEngine(db_instance=db)
job_manager = JobManager(db_instance=db, ai_engine=ai_engine)

consumer = KafkaConsumer(
    "resume_uploaded",
    bootstrap_servers="localhost:9092",
    group_id="job_processor_group",
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

logger.info("Worker started. Listening for messages...")

for message in consumer:
    data = message.value
    user_id = data.get("user_id")
    resume = data.get("resume")
    
    logger.info(f"Processing resume for user: {user_id}")
    
    try:
        # 1. AI Extraction
        ai_engine.extract_resume_tags(user_id, resume)
        
        # 2. Match Jobs
        job_manager.fetch_and_store_jobs(user_id, "Stockholm")
        
        logger.info(f"Successfully processed user {user_id}")
    except Exception as e:
        logger.error(f"Error processing user {user_id}: {e}")