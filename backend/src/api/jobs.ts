import { Hono } from 'hono';
import axios from 'axios';
import { db } from '../db/firebaseAdmin.js';

const jobs = new Hono();
const PYTHON_URL = 'http://127.0.0.1:8000';

jobs.post('/fetch', async (c) => {
    try {
        const body = await c.req.json();
        const municipality = body['municipality'] as string;
        const userId = body['user_id'] as string;

        const pythonResponse = await axios.post(`${PYTHON_URL}/api/fetchjobs`, {
        user_id: userId,
        municipality: municipality
        });
        return c.json({
            message: "Job fetch successful",
            python_response: pythonResponse.data
        });

    } catch (error: any) {
        console.error("Fetch Error:", error.message);
        return c.json({ error: "Failed to fetch jobs", details: error.message }, 500);
    }
});

jobs.post('/match', async (c) => {
    try {
        const body = await c.req.json();
        const userId = body['user_id'] as string;

        const pythonResponse = await axios.post(`${PYTHON_URL}/api/matchjobs`, {
        user_id: userId,
        municipality: "all"
        });
        return c.json({
            message: "Job match successful",
            python_response: pythonResponse.data
        });

    } catch (error: any) {
        console.error("Match Error:", error.message);
        return c.json({ error: "Failed to match jobs", details: error.message }, 500);
    }
});

jobs.post('get', async (c) => {
    try {
        // Note: If this is a GET request, consider c.req.query('user_id') 
        // if c.req.json() gives you issues.
        const body = await c.req.json();
        const userId = body['user_id'] as string;

        // 1. Create a query ordered by the "match_percentage" key
        const educationRef = db.ref(`${userId}/jobs/education`);
        const query = educationRef.orderByChild('match_percentage');

        const snapshot = await query.once('value');

        if (!snapshot.exists()) {
            return c.json({ data: [] }, 200);
        }

        const educationList: any[] = [];

        // 2. Use .forEach() - THIS IS REQUIRED FOR SORTING
        // snapshot.val() returns a JSON object which loses the order.
        // .forEach() guarantees the order defined in your query.
        snapshot.forEach((childSnapshot) => {
            educationList.push({
                id: childSnapshot.key,
                ...childSnapshot.val()
            });
        });

        // 3. Firebase is ascending only. For "highest match first", reverse the array.
        const sortedDesc = educationList.reverse();

        return c.json({ data: sortedDesc }, 200);

    } catch (error: any) {
        console.error("Fetch Error:", error.message);
        return c.json({ error: "Failed to fetch jobs", details: error.message }, 500);
    }
});

export default jobs;