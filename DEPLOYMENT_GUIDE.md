# 🚀 Secure Deployment Guide for Firebase

## ⚠️ CRITICAL SECURITY ISSUES FIXED

### 1. **Rate Limiting Added**
- **Game moves**: 60/minute per IP
- **Game state**: 30/minute per IP  
- **Reset game**: 10/minute per IP
- **Player types**: 10/minute per IP

### 2. **Input Validation**
- Pydantic models validate all inputs
- Move indices must be 0-8
- Player types must be valid
- Encoded state format validation

### 3. **CORS Security**
- Environment-based origin configuration
- Removed wildcard methods/headers
- Production origins only in production

### 4. **Error Handling**
- Internal errors logged but not exposed
- Generic error messages to clients
- Proper HTTP status codes

## 🏗️ DEPLOYMENT ARCHITECTURE

### Frontend (Firebase Hosting)
```
Firebase Hosting → Static React App
```

### Backend (Google Cloud Run)
```
Google Cloud Run → FastAPI Backend
```

## 📋 DEPLOYMENT STEPS

### 1. **Backend Deployment (Google Cloud Run)**

```bash
# Build and deploy backend
cd backend
gcloud run deploy tic-tac-toe-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production,ALLOWED_ORIGINS=https://your-app.web.app
```

### 2. **Frontend Deployment (Firebase Hosting)**

```bash
# Build frontend
cd frontends/web
npm run build

# Deploy to Firebase
firebase deploy --only hosting
```

### 3. **Environment Variables**

#### Backend (.env)
```env
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-app.web.app,https://your-app.firebaseapp.com
PORT=8080
```

#### Frontend (.env.production)
```env
VITE_API_URL=https://your-backend-url.run.app
```

## 🔒 SECURITY CHECKLIST

- ✅ Rate limiting implemented
- ✅ Input validation added
- ✅ CORS properly configured
- ✅ Error handling secured
- ✅ Security headers added
- ✅ Environment-based configuration
- ✅ No hardcoded URLs in production

## 🚨 BEFORE DEPLOYING

1. **Update CORS origins** in backend environment
2. **Set production API URL** in frontend environment
3. **Test rate limiting** doesn't break normal usage
4. **Verify security headers** are working
5. **Test error handling** doesn't leak information

## 📊 MONITORING

Monitor these metrics after deployment:
- API response times
- Rate limit hits
- Error rates
- Resource usage (especially AlphaZero)

## 🛡️ ADDITIONAL SECURITY RECOMMENDATIONS

1. **Add authentication** if you want user accounts
2. **Implement request logging** for monitoring
3. **Add health checks** for load balancers
4. **Consider CDN** for static assets
5. **Set up monitoring alerts** for unusual traffic

## 🔧 TROUBLESHOOTING

### Common Issues:
- **CORS errors**: Check ALLOWED_ORIGINS environment variable
- **Rate limiting**: Adjust limits if too restrictive
- **API not found**: Verify Cloud Run URL is correct
- **Build failures**: Check Node.js/Python versions

### Support:
- Check Cloud Run logs: `gcloud logs read`
- Check Firebase hosting logs in Firebase Console
- Monitor API metrics in Google Cloud Console
