import { Hono } from 'hono';
import axios from 'axios';

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

export default jobs;