import { Hono } from 'hono';
import { serve } from '@hono/node-server';
import { swaggerUI } from '@hono/swagger-ui';
import { cors } from 'hono/cors';
import resume from './api/resume.js';
import jobs from './api/jobs.js';
import { initKafka } from './kafka';
import { logger } from './logger';

const app = new Hono();
const PYTHON_URL = 'http://127.0.0.1:8000';
initKafka().catch(err => logger.error(err, 'Kafka initialization failed'));

app.use('/api/*', cors({
  origin: 'http://localhost:5173',
  allowMethods: ['POST', 'GET', 'OPTIONS'],
}));

app.route('/api', resume);
app.route('/api', jobs);

// Opens swagger.ui
app.get('/openapi.json', (c) => {
  return c.json({
    openapi: '3.0.0',
    info: {
      title: 'Annonskollen Gateway API',
      version: '1.0.0',
      servers: [
        {
          url: 'http://localhost:3000',
          description: 'Local Development Server'
        }
      ],
    },
    paths: {
      '/api/upload': {
        post: {
          summary: 'Upload and Extract PDF',
          requestBody: {
            required: true,
            content: {
              'multipart/form-data': {
                schema: {
                  type: 'object',
                  properties: {
                    user_id: { type: 'string', example: 'anna_123' },
                    file: { type: 'string', format: 'binary', description: 'The PDF resume file' }
                  },
                  required: ['user_id', 'file']
                }
              }
            }
          },
          responses: { 200: { description: 'Extraction successful' } },
        },
      },
      '/api/fetch': {
        post: {
          summary: 'Fetches relevant jobs',
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    user_id: { type: 'string', example: 'anna_123' },
                    municipality: { type: 'string', example: 'Linköping' }
                  },
                  required: ['user_id', 'municipality']
                }
              }
            }
          },
          responses: { 200: { description: 'Jobs fetched successfully' } },
        },
      },
      '/api/match': {
        post: {
          summary: 'Matches user with jobs',
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    user_id: { type: 'string', example: 'anna_123' }
                  },
                  required: ['user_id']
                }
              }
            }
          },
          responses: { 200: { description: 'Matching process started' } },
        },
      },
      '/api/get': {
        post: {
          summary: 'Fetch matched jobs, matched percentage ascending order',
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    user_id: { type: 'string', example: 'anna_123' }
                  },
                  required: ['user_id']
                }
              }
            }
          },
          responses: { 200: { description: 'Jobs fetched successfully' } },
        },
      },
    },
  });
});

app.get('/docs', swaggerUI({ url: '/openapi.json' }));


console.log('Swagger UI available at http://localhost:3000/docs');
serve({ fetch: app.fetch, port: 3000 });