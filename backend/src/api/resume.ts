import { Hono } from 'hono';
import axios from 'axios';
import PdfParse from 'pdf-parse-new';
import { produceEvent } from '../kafka';
import { logger } from '../logger';

const resume = new Hono();
const PYTHON_URL = 'http://127.0.0.1:8000';

resume.post('/upload', async (c) => {
  try {
    const body = await c.req.parseBody();
    const file = body['file'] as File;
    const userId = body['user_id'] as string;
    if (!file) return c.json({ error: "No file uploaded" }, 400);

    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    const pdfData = await PdfParse(buffer);
    const extractedText = pdfData.text;

    logger.info({ userId }, "Triggering upload and tag extraction via Kafka");
    await produceEvent('resume_uploaded', { 
      user_id: userId, 
      resume: extractedText
    });

    return c.json({
      status: "accepted"
    }, 202);

  } catch (error: any) {
        logger.error({ error: error.message }, "Kafka upload and tag extraction Trigger Error");
        return c.json({ error: "Failed to queue fetch job" }, 500);
    }
});

export default resume;