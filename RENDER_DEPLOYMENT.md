# Deploy to Render.com

## Overview
Render is a modern cloud platform perfect for deploying Flask apps with environment variables. Your app will be live and accessible 24/7.

## Step 1: Prepare Your Repository

Your repo is already set up for Render! Key files:
- `app.py` — Flask app
- `requirements.txt` — Python dependencies
- `Procfile` — Render deployment instructions (we'll create this)
- `.env.example` — Environment variable template

## Step 2: Create Procfile

Create a `Procfile` in your project root (tells Render how to run the app):

```
web: gunicorn app:app
```

Add `gunicorn` to `requirements.txt`:
```
gunicorn
```

## Step 3: Prepare Render Environment Variables

Go to Render dashboard and set these environment variables:

1. **GOOGLE_SPREADSHEET_ID**
   - Value: Your Google Sheets ID (e.g., `1A3bC4dEfG5hIjKlMnOpQrStUvWxYz6`)

2. **GOOGLE_SHEET_NAME**
   - Value: `Members`

3. **GOOGLE_CREDENTIALS_JSON**
   - Value: Your full credentials.json as a single-line JSON string
   
   **To convert:**
   ```powershell
   # PowerShell (Windows)
   (Get-Content -Path credentials.json -Raw) | ConvertFrom-Json | ConvertTo-Json -Compress
   ```
   
   Then copy the entire output and paste into Render

## Step 4: Deploy to Render

1. Go to https://render.com
2. Sign up or log in
3. Click "New +" > "Web Service"
4. Connect your GitHub repository (Elghouali/N7_Club_Kiosk)
5. Configure:
   - **Name:** `n7-club-kiosk`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free tier is available
6. Click "Create Web Service"

Render will automatically:
- Install dependencies
- Run your Flask app
- Deploy it globally
- Assign you a live URL (e.g., `https://n7-club-kiosk.onrender.com`)

## Step 5: Add Environment Variables to Render

1. Go to your Render dashboard
2. Click on your service: `n7-club-kiosk`
3. Click "Environment" in the left sidebar
4. Add the 3 environment variables:
   - `GOOGLE_SPREADSHEET_ID`
   - `GOOGLE_SHEET_NAME` 
   - `GOOGLE_CREDENTIALS_JSON`
5. Click "Save"
6. The app will automatically redeploy

## Step 6: Test Your Live App

1. Visit your Render URL: `https://n7-club-kiosk.onrender.com`
2. Fill out the form and click "JOIN THE CLUB"
3. Data should be saved to your Google Sheet immediately ✓

## Step 7: Share Your App

Your live app URL can be shared anywhere. The form submission endpoint is at:
```
POST https://n7-club-kiosk.onrender.com/submit
```

## GitHub Pages (Optional)

For GitHub Pages to automatically update member count:

1. Set the same secrets on GitHub:
   - `GOOGLE_SPREADSHEET_ID`
   - `GOOGLE_CREDENTIALS_JSON`

2. Your GitHub Actions workflow will:
   - Run on every push to master
   - Export static HTML with live member count
   - Publish to GitHub Pages

## Architecture

```
User fills form at:
    https://n7-club-kiosk.onrender.com
           ↓
    Flask app processes request
           ↓
    Saves to Google Sheets (real-time)
           ↓
    
GitHub Pages (optional):
    https://elghouali.github.io/N7_Club_Kiosk/
           ↓
    Static site (exported on each push)
           ↓
    Shows member count (updates hourly via CI/CD)
```

## Troubleshooting

### App won't deploy
- Check build logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Make sure `app.py` has `if __name__ == '__main__'` block

### "GOOGLE_CREDENTIALS_JSON not set"
- Verify you added the environment variable to Render
- Make sure it's valid JSON (use the command above to compress)
- Don't include newlines

### Form submissions fail
- Check Render logs: Dashboard → Service → Logs
- Verify Google Sheets ID is correct
- Check that service account has sheet access

### Rate limiting
- Free tier has some limits, but suitable for most use cases
- Consider upgrading if you need more capacity

## Costs

- **Free tier:** 0.50 CPU, 512 MB RAM (sleeps after inactivity)
- **Paid tier:** From $7/month with persistent uptime
- Upgrade anytime from Render dashboard

## Local Testing Before Deployment

Test locally with `.env`:
```
GOOGLE_SPREADSHEET_ID=your_id
GOOGLE_SHEET_NAME=Members
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
```

Then run:
```
python app.py
```

Visit `http://localhost:5000` and test the form.
