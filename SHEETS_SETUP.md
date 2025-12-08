# N7 Club Kiosk - Google Sheets Integration Guide

## Setup Steps

### 1. Create a Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create a Service Account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the form and click "Create"
5. Create a JSON key:
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key" > JSON
   - Download the JSON file and save as `credentials.json` in the project root

### 2. Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet (name it "N7 Club Members" or similar)
3. The first sheet tab will be used automatically (rename to "Members" if desired)
4. Copy the spreadsheet ID from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

### 3. Share the Sheet with the Service Account

1. Open your Google Sheet
2. Click the "Share" button (top right)
3. Copy the email from your `credentials.json` file (looks like `service-account-name@project-id.iam.gserviceaccount.com`)
4. Paste it in the share dialog and grant "Editor" access
5. Don't send notifications

### 4. Configure the Application

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your values:
   ```
   GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_from_step_2
   GOOGLE_SHEET_NAME=Members
   GOOGLE_CREDENTIALS_PATH=credentials.json
   ```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

The Flask app will:
- Initialize Google Sheets connection on startup
- Create headers automatically if they don't exist
- Save all member submissions to Google Sheets in real-time

## Troubleshooting

### "Credentials file not found"
- Make sure `credentials.json` is in the project root
- Check the path in `.env`

### "The caller does not have permission to access the file"
- Make sure you shared the Google Sheet with the service account email
- Verify the service account has "Editor" access

### "Invalid Spreadsheet ID"
- Copy the ID directly from the Google Sheets URL
- Format should be a long alphanumeric string

## Local Development

For local testing without Google Sheets, comment out the `init_google_sheets()` call in `app.py`. The app will still run but member data won't persist.
