import { Hono } from 'hono';
import { db } from '../db/firebaseAdmin.js';
import { produceEvent } from '../kafka';
import { logger } from '../logger';

const jobs = new Hono();
const PYTHON_URL = 'http://127.0.0.1:8000';

jobs.post('/fetch', async (c) => {
    try {
        const body = await c.req.json();
        const municipality = body['municipality'] as string;
        const userId = body['user_id'] as string;

        logger.info({ userId, municipality }, "Triggering job fetch via Kafka");

        await produceEvent('fetch_job', { 
            user_id: userId, 
            municipality: municipality 
        });

        return c.json({
            status: "accepted"
        }, 202);

    } catch (error: any) {
        logger.error({ error: error.message }, "Kafka Fetch Trigger Error");
        return c.json({ error: "Failed to queue fetch job" }, 500);
    }
});

jobs.post('/match', async (c) => {
    try {
        const body = await c.req.json();
        const userId = body['user_id'] as string;

        logger.info({ userId }, "Triggering job match via Kafka");

        await produceEvent('match_job', { 
            user_id: userId
        });

        return c.json({
            status: "accepted"
        }, 202);

    } catch (error: any) {
        logger.error({ error: error.message }, "Kafka Match Trigger Error");
        return c.json({ error: "Failed to queue match job" }, 500);
    }
});

jobs.post('get', async (c) => {
    try {
        const body = await c.req.json();
        const userId = body['user_id'] as string;

        logger.info({ userId }, "Fetching job info");

        const educationRef = db.ref(`${userId}/jobs/education`);
        const query = educationRef.orderByChild('match_percentage');

        const snapshot = await query.once('value');

        if (!snapshot.exists()) {
            return c.json({ data: [] }, 200);
        }

        const educationList: any[] = [];

        snapshot.forEach((childSnapshot) => {
            educationList.push({
                id: childSnapshot.key,
                ...childSnapshot.val()
            });
        });

        const sortedDesc = educationList.reverse();
        return c.json({ data: sortedDesc }, 200);

    } catch (error: any) {
        console.error("Fetch Error:", error.message);
        return c.json({ error: "Failed to fetch jobs", details: error.message }, 500);
    }
});

export default jobs;