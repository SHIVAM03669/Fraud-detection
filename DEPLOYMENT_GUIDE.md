# 🚀 Fraud Detection System - Deployment Guide

This guide provides multiple deployment options for your fraud detection system, from local development to cloud production.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ Trained model file (`models/fraud_model.pkl`)
- ✅ All dependencies in `requirements.txt`
- ✅ API and Dashboard code ready

## 🐳 Option 1: Docker (Recommended for Local/Self-Hosted)

### Quick Start
```bash
# Build and run both API and Dashboard
docker-compose up -d

# Access services
# API: http://localhost:8000
# Dashboard: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

### Individual Services
```bash
# Build the image
docker build -t fraud-detection .

# Run API only
docker run -p 8000:8000 fraud-detection

# Run Dashboard only
docker run -p 8501:8501 fraud-detection streamlit run dashboard/app.py --server.address 0.0.0.0
```

### Production Docker
```bash
# For production, use docker-compose with environment variables
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## ☁️ Option 2: Cloud Platforms

### 2.1 Heroku (Easy, Free Tier Available)

```bash
# Install Heroku CLI first
# Copy Heroku files
cp deploy/heroku/Procfile .
cp deploy/heroku/runtime.txt .

# Create and deploy
heroku create your-fraud-api
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Scale the app
heroku ps:scale web=1
```

**Pros:** Easy setup, free tier, automatic SSL
**Cons:** Cold starts, limited free hours

### 2.2 Railway (Modern, Simple)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up

# Custom domain (optional)
railway domain
```

**Pros:** No cold starts, simple pricing, great DX
**Cons:** Newer platform, limited free tier

### 2.3 Render (GitHub Integration)

1. Connect your GitHub repository to Render
2. Upload `deploy/render/render.yaml` to your repo
3. Render will automatically deploy both services

**Pros:** Free tier, automatic deployments, SSL
**Cons:** Cold starts on free tier

### 2.4 AWS Lambda (Serverless)

```bash
# Create deployment package
mkdir lambda-deploy
cp -r api/ models/ lambda-deploy/
cp deploy/aws/app.py lambda-deploy/
cd lambda-deploy
pip install -r ../deploy/aws/requirements.txt -t .
zip -r fraud-detection-lambda.zip .
```

Upload to AWS Lambda:
1. Create new Lambda function
2. Upload the zip file
3. Set handler to `app.lambda_handler`
4. Configure API Gateway trigger

**Pros:** Pay per request, auto-scaling, no server management
**Cons:** Cold starts, size limits, complexity

### 2.5 Vercel (Frontend + API)

```bash
# Install Vercel CLI
npm install -g vercel

# Copy config and deploy
cp deploy/vercel/vercel.json .
vercel --prod
```

**Pros:** Great for full-stack apps, edge functions
**Cons:** Limited Python support, function timeouts

## 🔧 Environment Configuration

### Environment Variables

Create `.env` file for local development:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=models/fraud_model.pkl

# Dashboard Configuration
DASHBOARD_PORT=8501
API_URL=http://localhost:8000

# Production Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Production Considerations

1. **Security**
   - Use HTTPS in production
   - Set up proper CORS policies
   - Add API rate limiting
   - Use environment variables for secrets

2. **Performance**
   - Enable model caching
   - Use connection pooling
   - Set up health checks
   - Monitor response times

3. **Monitoring**
   - Add logging and metrics
   - Set up alerts for errors
   - Monitor model performance
   - Track API usage

## 📊 Monitoring & Health Checks

### Health Check Endpoints
- API Health: `GET /health`
- Model Status: `GET /health` (includes model_loaded status)

### Logging
```python
# API logs prediction requests
# Dashboard logs user interactions
# Monitor for errors and performance
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy Fraud Detection
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway deploy
```

## 🚨 Troubleshooting

### Common Issues

1. **Model Not Loading**
   - Check file path: `models/fraud_model.pkl`
   - Verify model was trained and saved
   - Check file permissions

2. **Import Errors**
   - Ensure all dependencies in `requirements.txt`
   - Check Python version compatibility
   - Verify PYTHONPATH is set correctly

3. **API Connection Issues**
   - Check port configuration
   - Verify firewall settings
   - Test with curl: `curl http://localhost:8000/health`

4. **Dashboard Not Connecting to API**
   - Update API_URL in dashboard
   - Check CORS settings
   - Verify both services are running

### Performance Issues

1. **Slow Predictions**
   - Model loading on each request (cache it)
   - Large model size (consider model compression)
   - Network latency (deploy closer to users)

2. **Memory Issues**
   - Increase container memory limits
   - Optimize model size
   - Use model quantization

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers
- Deploy multiple API instances
- Consider container orchestration (Kubernetes)

### Vertical Scaling
- Increase CPU/memory resources
- Use faster storage (SSD)
- Optimize model inference

### Database Integration
- Add PostgreSQL for logging predictions
- Store user feedback for model improvement
- Implement audit trails

## 🔐 Security Best Practices

1. **API Security**
   - Add authentication (JWT tokens)
   - Implement rate limiting
   - Validate all inputs
   - Use HTTPS only

2. **Model Security**
   - Protect model files
   - Monitor for adversarial attacks
   - Implement input validation
   - Log suspicious requests

3. **Infrastructure Security**
   - Use secrets management
   - Regular security updates
   - Network segmentation
   - Access controls

## 📞 Support

For deployment issues:
1. Check the logs first
2. Verify all prerequisites
3. Test locally before deploying
4. Check platform-specific documentation

## 🎯 Quick Deployment Commands

```bash
# Local development
docker-compose up -d

# Heroku
git push heroku main

# Railway
railway up

# Vercel
vercel --prod

# AWS Lambda
# Upload dist/fraud-detection-lambda.zip to AWS Console
```

Choose the deployment option that best fits your needs, budget, and technical requirements!