
# Project overview
Jobbannonskollen automates your job search by matching your resume to live openings in real-time. Instead of endless scrolling, our AI instantly identifies and scores the best opportunities for your profile, ensuring you only apply to the roles where you are a top-tier candidate.


## 🛠 Prerequisites

Before starting, ensure you have the following installed:
- **Docker & Docker Compose** (Required for Kafka & Zookeeper)
- **Python 3.12+**
- **Node.js 20+**
- **Firebase Account** (Service Account Key)

---

## 🏗 Project Structure

- **/app**: FastAPI AI Engine and business logic.
- **/app/worker.py**: Background Python consumer processing Kafka tasks.
- **/backend**: Node.js (Hono/TypeScript) orchestrator and API gateway.
- **/docker-compose.yml**: Infrastructure setup for the Kafka broker.

---

# 🚀 Setup & Installation

## 1. Infrastructure (Kafka)
Start the message broker. This must be running for the backend and workers to communicate.
```bash
docker-compose up -d
```

## 2. Python Environment (AI Engine)

### Create the environment
```
python3 -m venv .venv
```

### Activate (Linux/macOS)
```
source .venv/bin/activate
```

### Activate (Windows)
```
.venv\Scripts\activate
```

## 3. Node.js Backend
Install the dependencies for the Hono gateway:

```
cd backend
npm install
cd ..
```

## 4. Running the system
```
npm run dev
```

# Configuration

## Firebase
Ensure you have your Firebase credentials placed in the correct directory. Do not commit this file to version control.

Path: app/db/firebase-adminsdk.json

## Environment Variables
Check that your .env files are configured in both the root and /backend folders for:

API Keys (OpenAI/Anthropic)

Kafka Broker URLs

Database URLs