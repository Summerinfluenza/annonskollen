import admin from 'firebase-admin';
import * as path from 'path';
import * as dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { readFileSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const databaseURL = process.env.DATABSE_URL;
const serviceAccountPath = process.env.FIREBASE_SERVICE_ACCOUNT_PATH;

if (!serviceAccountPath || !databaseURL) {
  throw new Error("Missing Firebase configuration in environment variables");
}

const serviceAccount = JSON.parse(
  readFileSync(path.resolve(__dirname, '../../', serviceAccountPath), 'utf8')
);

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: databaseURL
});

export const db = admin.database();