# Deployment Guide - Render

## Step 1: Prepare Your Code

1. **Push to GitHub** (if you haven't already):
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

## Step 2: Deploy to Render

1. **Sign up** at [render.com](https://render.com) (free account)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your repository

3. **Configure Service**:
   - **Name**: `pantry-commissary-system`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/app.py`

4. **Set Environment Variables**:
   - Go to "Environment" tab
   - Add: `SPOONACULAR_API_KEY` = `your_api_key_here`
   - Add: `FLASK_DEBUG` = `false`

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

## Step 3: Access Your App

Your app will be available at: `https://your-service-name.onrender.com`

The frontend will be served at the root URL, and the API will be available at `/api/` endpoints.

## Step 4: Test Your Deployment

1. Visit your app URL
2. Check that ingredient data loads (should show 218 pantry + 1242 commissary items)
3. Try searching for recipes
4. Verify detailed grocery lists work

## Troubleshooting

- **App won't start**: Check logs in Render dashboard
- **API errors**: Verify SPOONACULAR_API_KEY is set correctly
- **No recipes found**: Check API key is valid and has remaining calls

## Free Tier Limitations

- App may sleep after 15 minutes of inactivity (wakes up in ~30 seconds)
- 750 hours per month (sufficient for personal use)
- Automatic HTTPS included

## Cost

- **Free tier**: $0/month
- **Paid tier**: $7/month (if you need always-on service)