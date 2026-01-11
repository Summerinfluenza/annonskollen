import { Hono } from 'hono';
import axios from 'axios';
import PdfParse from 'pdf-parse-new';

const resume = new Hono();
const PYTHON_URL = 'http://127.0.0.1:8000';

resume.post('/api/upload', async (c) => {
  try {
    const body = await c.req.parseBody();
    const file = body['file'] as File;
    const userId = body['user_id'] as string;

    if (!file) return c.json({ error: "No file uploaded" }, 400);

    // 1. Convert file to Buffer
    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // 2. Extract text from PDF
    const pdfData = await PdfParse(buffer);
    const extractedText = pdfData.text;

    console.log(`Extracted ${extractedText.length} characters for user ${userId}`);

    // 3. Send the STRING to Python
    // We change the Python call to a simple JSON POST instead of multipart
    const pythonResponse = await axios.post(`${PYTHON_URL}/api/createusertags`, {
      user_id: userId,
      resume: extractedText
    });

    return c.json({
      message: "Extraction successful",
      python_response: pythonResponse.data
    });

  } catch (error: any) {
    console.error("Extraction Error:", error.message);
    return c.json({ error: "Failed to parse PDF", details: error.message }, 500);
  }
});

export default resume;