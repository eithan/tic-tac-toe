# 📋 Installation Steps for Google Cloud Run Deployment

## 🔧 **Step 1: Install Google Cloud CLI**

### **macOS (using Homebrew):**
```bash
brew install google-cloud-sdk
```

### **macOS (manual install):**
```bash
# Download and install
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### **Alternative: Download from Google**
Visit: https://cloud.google.com/sdk/docs/install

## 🔐 **Step 2: Authenticate and Setup**

```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace with your actual project ID)
gcloud config set project ez-tic-tac-toe

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## 🚀 **Step 3: Deploy**

Once gcloud is installed and configured:

```bash
# Make the script executable (if not already)
chmod +x deploy.sh

# Deploy to Cloud Run
./deploy.sh
```

## 🧪 **Step 4: Test**

After deployment, test your API:

```bash
# Get your API URL
gcloud run services describe tic-tac-toe-api --region us-central1 --format 'value(status.url)'

# Test health endpoint
curl https://your-api-url/health
```

## 📊 **Step 5: Monitor**

- **Cloud Run Console**: https://console.cloud.google.com/run
- **Logs**: `gcloud run services logs read tic-tac-toe-api --region us-central1`
- **Metrics**: Available in Google Cloud Console

## 🎯 **Expected Results**

After successful deployment:
- ✅ API available at Cloud Run URL
- ✅ All endpoints working (health, game_state, game_move, etc.)
- ✅ AlphaZero player available
- ✅ Auto-scaling based on traffic
- ✅ Pay only for actual usage

## 🆘 **If You Need Help**

1. **Check logs**: `gcloud run services logs read tic-tac-toe-api --region us-central1`
2. **Verify project**: `gcloud config get-value project`
3. **Check authentication**: `gcloud auth list`
4. **View service status**: `gcloud run services describe tic-tac-toe-api --region us-central1`
