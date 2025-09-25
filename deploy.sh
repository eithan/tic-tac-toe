#!/bin/bash

# Deploy Tic-Tac-Toe API to Google Cloud Run
# This script ensures ALLOWED_ORIGINS is always set to include Firebase Hosting

set -e  # Exit on any error

echo "🚀 Deploying Tic-Tac-Toe API to Google Cloud Run..."

# Set the Firebase Hosting URL as the primary allowed origin
FIREBASE_URL="https://ez-tic-tac-toe.web.app"

# Deploy with the Firebase URL in ALLOWED_ORIGINS
gcloud run deploy tic-tac-toe-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 4Gi \
  --cpu 2 \
  --max-instances 5 \
  --set-env-vars "ENVIRONMENT=production,ALLOWED_ORIGINS=${FIREBASE_URL}" \
  --timeout 900

echo "✅ Deployment complete!"
echo "🌐 API URL: https://tic-tac-toe-api-1063248455981.us-central1.run.app"
echo "🔗 Frontend URL: ${FIREBASE_URL}"
echo "🔒 CORS configured for: ${FIREBASE_URL}"