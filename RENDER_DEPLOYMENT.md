# Render Deployment Guide

## Prerequisites

1. **PostgreSQL Database**: Create a PostgreSQL database service on Render
2. **Web Service**: Deploy your FastAPI backend as a web service

## Step 1: Create PostgreSQL Database

1. Go to your Render dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `compliance-db` (or your preferred name)
   - **Database**: `compliance_db`
   - **User**: `compliance_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free tier is fine for development

4. After creation, note down the **External Database URL** from the database dashboard

## Step 2: Deploy Backend Service

1. Go to your Render dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

### Build & Deploy Settings:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Environment Variables:
Set these in the Render dashboard under "Environment":

```bash
# Database (CRITICAL - This is the main issue)
DATABASE_URL=postgresql://compliance_user:password@dpg-xxxxx-a/compliance_db
# ^ Use the External Database URL from your PostgreSQL service

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://compliance-frontend.onrender.com,https://compliance-ui.onrender.com,https://compliance-ui.netlify.app

# Environment
ENVIRONMENT=production
DEBUG=false

# Render specific
RENDER=true
```

## Step 3: Important Notes

### Database URL Format:
The DATABASE_URL should look like:
```
postgresql://username:password@hostname:port/database_name
```

### Common Issues:

1. **Connection Refused Error**: 
   - Make sure you're using the External Database URL, not Internal
   - Check that the DATABASE_URL environment variable is set correctly

2. **CORS Issues**:
   - Add your frontend URL to ALLOWED_ORIGINS
   - Use comma-separated values in Render environment variables

3. **Port Issues**:
   - Render automatically sets the PORT environment variable
   - Use `$PORT` in your start command

## Step 4: Verify Deployment

1. Check the service logs for any errors
2. Visit `https://your-service-name.onrender.com/health` to verify database connection
3. Visit `https://your-service-name.onrender.com/docs` to see the API documentation

## Step 5: Frontend Configuration

Update your frontend to use the new backend URL:
- Change API base URL to `https://your-service-name.onrender.com/api/v1`

## Troubleshooting

### Database Connection Issues:
1. Verify DATABASE_URL is set correctly
2. Check that the PostgreSQL service is running
3. Ensure the database credentials are correct

### Build Issues:
1. Check that all dependencies are in requirements.txt
2. Verify the build command is correct
3. Check the build logs for specific errors

### Runtime Issues:
1. Check the service logs
2. Verify all environment variables are set
3. Test the health endpoint

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@host:port/db |
| SECRET_KEY | JWT secret key | your-secret-key-here |
| ALLOWED_ORIGINS | CORS allowed origins | https://frontend.onrender.com |
| ENVIRONMENT | Environment name | production |
| DEBUG | Debug mode | false |
