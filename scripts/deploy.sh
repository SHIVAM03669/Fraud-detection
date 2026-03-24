#!/bin/bash

# Fraud Detection System Deployment Script
# Usage: ./scripts/deploy.sh [platform]
# Platforms: docker, heroku, railway, render, aws

set -e

PLATFORM=${1:-docker}
PROJECT_NAME="fraud-detection"

echo "🚀 Deploying Fraud Detection System to $PLATFORM"

case $PLATFORM in
  "docker")
    echo "📦 Building and running with Docker Compose..."
    docker-compose down --remove-orphans
    docker-compose build --no-cache
    docker-compose up -d
    echo "✅ Deployed! API: http://localhost:8000, Dashboard: http://localhost:8501"
    ;;
    
  "heroku")
    echo "☁️ Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
      echo "❌ Heroku CLI not found. Please install it first."
      exit 1
    fi
    
    # Copy Heroku files to root
    cp deploy/heroku/Procfile .
    cp deploy/heroku/runtime.txt .
    
    # Create Heroku apps
    heroku create $PROJECT_NAME-api --region us
    heroku create $PROJECT_NAME-dashboard --region us
    
    # Deploy API
    git subtree push --prefix=. heroku-api main || git push heroku-api main
    
    echo "✅ Deployed to Heroku!"
    echo "API: https://$PROJECT_NAME-api.herokuapp.com"
    echo "Dashboard: https://$PROJECT_NAME-dashboard.herokuapp.com"
    ;;
    
  "railway")
    echo "🚂 Deploying to Railway..."
    
    if ! command -v railway &> /dev/null; then
      echo "❌ Railway CLI not found. Please install it first."
      exit 1
    fi
    
    cp deploy/railway/railway.toml .
    railway login
    railway link
    railway up
    
    echo "✅ Deployed to Railway!"
    ;;
    
  "render")
    echo "🎨 Deploying to Render..."
    echo "Please upload the deploy/render/render.yaml file to your Render dashboard"
    echo "Or connect your GitHub repository to Render"
    ;;
    
  "aws")
    echo "☁️ Preparing AWS Lambda deployment..."
    
    # Create deployment package
    mkdir -p dist/aws
    cp -r api/ dist/aws/
    cp -r models/ dist/aws/
    cp deploy/aws/app.py dist/aws/
    cp deploy/aws/requirements.txt dist/aws/
    
    cd dist/aws
    pip install -r requirements.txt -t .
    zip -r ../fraud-detection-lambda.zip .
    cd ../..
    
    echo "✅ AWS Lambda package created: dist/fraud-detection-lambda.zip"
    echo "Upload this to AWS Lambda and set handler to 'app.lambda_handler'"
    ;;
    
  "vercel")
    echo "▲ Deploying to Vercel..."
    
    if ! command -v vercel &> /dev/null; then
      echo "❌ Vercel CLI not found. Please install it first."
      exit 1
    fi
    
    cp deploy/vercel/vercel.json .
    vercel --prod
    
    echo "✅ Deployed to Vercel!"
    ;;
    
  *)
    echo "❌ Unknown platform: $PLATFORM"
    echo "Available platforms: docker, heroku, railway, render, aws, vercel"
    exit 1
    ;;
esac

echo "🎉 Deployment complete!"