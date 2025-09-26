#!/bin/bash

# Deploy Tic-Tac-Toe API with AlphaZero support to Google Cloud Run
# This script uses a multi-stage Docker build for ML dependencies

set -e  # Exit on any error

echo "🚀 Deploying Tic-Tac-Toe API with AlphaZero to Google Cloud Run..."

# Set the Firebase Hosting URL as the primary allowed origin
FIREBASE_URL="https://ez-tic-tac-toe.web.app"

# First, rename the Dockerfile temporarily
cp Dockerfile Dockerfile.backup
cp Dockerfile.alphazero Dockerfile

# Deploy with the Firebase URL in ALLOWED_ORIGINS and increased resources for ML
gcloud run deploy tic-tac-toe-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 8Gi \
  --cpu 4 \
  --max-instances 3 \
  --set-env-vars "ENVIRONMENT=production,ALLOWED_ORIGINS=${FIREBASE_URL}" \
  --timeout 3600

# Restore the original Dockerfile
mv Dockerfile.backup Dockerfile

echo "✅ AlphaZero deployment complete!"
echo "🌐 API URL: https://tic-tac-toe-api-1063248455981.us-central1.run.app"
echo "🔗 Frontend URL: ${FIREBASE_URL}"
echo "🔒 CORS configured for: ${FIREBASE_URL}"
echo "🤖 AlphaZero player should now be available!"
