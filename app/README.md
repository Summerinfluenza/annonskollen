# Create the environment
```
python3 -m venv .venv
```

# Activate (Linux/macOS)
```
source .venv/bin/activate
```

# Activate (Windows)
```
.venv\Scripts\activate
```

# Install Dependencies
```
pip install -r requirements.txt
```

# Create a .env file in the app directory:
```
GEMINI_API_KEY=your_key_here
```

# Create a firebase readltime database and generate a private key. Download and place the json file in app/db.

# Run the app in root directory:

```
uvicorn app.main:app --reload
```

# API Documentation
Once running, you can access the interactive Swagger UI to test all endpoints:
http://127.0.0.1:8000/docs

Method  Endpoint                Description
POST    /api/createusertags    #Uploads PDF, extracts text, and tags user via AI.
POST    /api/fetchjobs         #Scrapes current job ads for a specific municipality.
POST    /api/matchjobs         #Runs background AI task to match resume tags to jobs.