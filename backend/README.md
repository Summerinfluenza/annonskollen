## Install Dependencies
```
npm install
```

## API Documentation
Once running, you can access the interactive Swagger UI to test all endpoints:
http://127.0.0.1:3000/docs
```
Method  Endpoint                Description
POST    /api/resume/upload     #Uploads PDF, extracts text, and tags user via AI.
POST    /api/jobs/fetch        #Scrapes current job ads for a specific  municipality.
POST    /api/jobs/match        #Runs background AI task to match resume tags to jobs.
```