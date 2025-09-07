# Backend Deployment Guide

## Deploying to Render.com

### Prerequisites
- GitHub repository with your backend code
- Render.com account

### Deployment Steps

#### Option 1: Using Render Blueprint (Recommended)
1. Push your backend code to GitHub
2. Connect your repository to Render
3. Choose "Deploy from Blueprint"
4. Render will automatically use the `render.yaml` file to create all services

#### Option 2: Manual Deployment
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.11

### Environment Variables

The following environment variables will be set automatically by Render:

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string  
- `SECRET_KEY` - Auto-generated secret key
- `ENVIRONMENT=production`
- `DEBUG=false`

### Manual Environment Variables (if needed)

Add these in Render dashboard if you need them:

- `ALLOWED_ORIGINS` - Your frontend URL (e.g., `["https://your-frontend.netlify.app"]`)
- `MAIL_USERNAME` - Email service username
- `MAIL_PASSWORD` - Email service password
- `OPENAI_API_KEY` - OpenAI API key for AI features

### Database Setup

The `render.yaml` will automatically create:
- PostgreSQL database (`compliance-db`)
- Redis cache (`compliance-redis`)

### Health Check

After deployment, check:
- `https://your-backend-url.onrender.com/health` - Should show database connection status
- `https://your-backend-url.onrender.com/docs` - API documentation

### Troubleshooting

1. **Database Connection Issues**: Check the `/health` endpoint
2. **Build Failures**: Check the build logs in Render dashboard
3. **Environment Variables**: Verify all required variables are set

### Frontend Integration

Update your frontend's API URL to point to your deployed backend:
```
REACT_APP_API_URL=https://your-backend-url.onrender.com/api/v1
```
