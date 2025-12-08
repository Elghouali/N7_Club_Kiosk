# Quick Setup Guide

## You have credentials.json! ✓

Now you need to complete the setup:

### Step 1: Get Your Google Sheets ID

1. Go to Google Sheets: https://sheets.google.com
2. Create a new spreadsheet (name it "N7 Club Members")
3. Copy the ID from the URL:
   - URL: `https://docs.google.com/spreadsheets/d/{ID}/edit`
   - Copy the ID (long alphanumeric string)

### Step 2: Share the Sheet with Service Account

1. Click "Share" button on your Google Sheet
2. Copy this email from your credentials.json:
   ```
   zakariae@sound-berm-480611-c6.iam.gserviceaccount.com
   ```
3. Paste it into the share dialog
4. Give "Editor" access
5. Don't send notifications

### Step 3: Update .env File

Edit `.env` in your project root and replace:
```
GOOGLE_SPREADSHEET_ID=your_google_sheets_id_here
```

With your actual ID from Step 1.

### Step 4: Install Dependencies & Run

```powershell
pip install -r requirements.txt
python app.py
```

Then visit: http://localhost:5000

### Troubleshooting

**"Credentials file not found"**
- Make sure `credentials.json` is in the project root

**"The caller does not have permission"**
- Make sure you shared the Google Sheet with the service account email
- Sheet must be shared with "Editor" access

**"Invalid Spreadsheet ID"**
- Copy the ID from the URL bar (not the name)
- Should be a long alphanumeric string like: `1A3bC4dEfG5hIjKlMnOpQrStUvWxYz6`

**Still getting connection error?**
- Check terminal output for error messages
- Make sure all environment variables are set correctly
- Verify credentials.json is valid JSON
