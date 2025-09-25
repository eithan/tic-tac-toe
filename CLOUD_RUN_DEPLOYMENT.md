# 🚀 Google Cloud Run Deployment Guide

## ✅ **Why Cloud Run is Better Than Firebase Functions**

| Feature | Firebase Functions | Google Cloud Run |
|---------|-------------------|------------------|
| **Setup Complexity** | ❌ Complex | ✅ Simple |
| **FastAPI Support** | ❌ Requires conversion | ✅ Native support |
| **Cold Start** | ❌ Slow (10+ seconds) | ✅ Fast (1-2 seconds) |
| **Resource Limits** | ❌ Limited | ✅ Configurable |
| **ML Dependencies** | ❌ Timeout issues | ✅ Works perfectly |
| **Debugging** | ❌ Difficult | ✅ Easy |
| **Production Ready** | ❌ Limited | ✅ Enterprise grade |

## 🛠️ **Prerequisites**

1. **Install Google Cloud CLI:**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Enable APIs:**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

## 🚀 **Deployment Options**

### **Option 1: Quick Deploy (Recommended)**
```bash
./deploy.sh
```

### **Option 2: Manual Deploy**
```bash
gcloud run deploy tic-tac-toe-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars ENVIRONMENT=production
```

### **Option 3: Using Cloud Build**
```bash
gcloud builds submit --config cloudbuild.yaml
```

## 📋 **What Gets Deployed**

- ✅ **FastAPI Backend** - Your complete API
- ✅ **All Dependencies** - Including TensorFlow/OpenSpiel
- ✅ **AlphaZero Player** - Neural network support
- ✅ **Security Features** - CORS, rate limiting, etc.
- ✅ **Health Checks** - Monitoring endpoints

## 🌐 **API Endpoints**

Once deployed, your API will be available at:
```
https://tic-tac-toe-api-xxxxx-uc.a.run.app
```

**Available endpoints:**
- `GET /health` - Health check
- `POST /game_state` - Get/create game state
- `POST /game_move` - Make a move
- `POST /reset_game` - Reset game
- `GET /player_types` - Available player types

## 🧪 **Testing Your Deployment**

```bash
# Test health endpoint
curl https://your-api-url/health

# Test game state
curl -X POST https://your-api-url/game_state \
  -H "Content-Type: application/json" \
  -d '{}'

# Test game move
curl -X POST https://your-api-url/game_move \
  -H "Content-Type: application/json" \
  -d '{
    "move": {"index": 0},
    "encoded_state": "eyJib2FyZCI6IFsiIiwgIiIsICIiLCAiIiwgIiIsICIiLCAiIiwgIiIsICIiXSwgImN1cnJlbnRfcGxheWVyIjogIlgiLCAic3RhdHVzIjogImluX3Byb2dyZXNzIiwgIm1lc3NhZ2UiOiAiUGxheWVyIFgncyB0dXJuIn0=",
    "player_types": {"x_player_type": "human", "o_player_type": "human"}
  }'
```

## 💰 **Cost Estimation**

**Cloud Run Pricing:**
- **Free tier**: 2 million requests/month
- **After free tier**: $0.40 per million requests
- **CPU/Memory**: Only pay when requests are active
- **Estimated cost**: $0-5/month for small usage

## 🔧 **Configuration Options**

### **Environment Variables**
```bash
--set-env-vars ENVIRONMENT=production,ALLOWED_ORIGINS=https://your-frontend.com
```

### **Resource Limits**
```bash
--memory 2Gi          # More memory for ML workloads
--cpu 2               # More CPU for faster processing
--max-instances 100   # Scale up for high traffic
```

### **Security**
```bash
--no-allow-unauthenticated  # Require authentication
--service-account=SERVICE_ACCOUNT  # Use specific service account
```

## 🚨 **Troubleshooting**

### **Build Fails**
```bash
# Check logs
gcloud builds log --stream

# Test locally
docker build -t test .
docker run -p 8080:8080 test
```

### **Deployment Fails**
```bash
# Check service status
gcloud run services describe tic-tac-toe-api --region us-central1

# View logs
gcloud run services logs read tic-tac-toe-api --region us-central1
```

### **API Not Responding**
```bash
# Check if service is running
gcloud run services list

# Test health endpoint
curl https://your-api-url/health
```

## 🎯 **Next Steps**

1. **Deploy**: Run `./deploy.sh`
2. **Test**: Verify all endpoints work
3. **Update Frontend**: Point to new API URL
4. **Monitor**: Check Cloud Run console for metrics
5. **Scale**: Adjust resources based on usage

## 🎉 **Benefits**

- ✅ **Reliable**: No more Firebase Functions issues
- ✅ **Fast**: Sub-second cold starts
- ✅ **Scalable**: Auto-scales with traffic
- ✅ **Cost-effective**: Pay only for usage
- ✅ **Production-ready**: Enterprise-grade platform
