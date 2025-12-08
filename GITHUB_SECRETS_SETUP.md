# GitHub Secrets Setup Guide

## What are GitHub Secrets?

GitHub Secrets are encrypted environment variables stored securely in your GitHub repository. They are:
- ✅ Only accessible to GitHub Actions workflows
- ✅ Encrypted at rest and in transit
- ✅ Never exposed in logs or code
- ✅ Safe for storing credentials, API keys, etc.

## How to Add Secrets to Your Repository

### Step 1: Go to Repository Settings
1. Navigate to your GitHub repository: https://github.com/Elghouali/N7_Club_Kiosk
2. Click **Settings** (top navigation bar)
3. On the left sidebar, click **Secrets and variables** > **Actions**

### Step 2: Create the Secrets

You need to add 2 secrets:

#### Secret 1: `GOOGLE_SPREADSHEET_ID`
1. Click **New repository secret** button
2. Name: `GOOGLE_SPREADSHEET_ID`
3. Value: Your Google Sheets ID (from the URL: `https://docs.google.com/spreadsheets/d/{ID}/edit`)
4. Click **Add secret**

#### Secret 2: `GOOGLE_CREDENTIALS_JSON`
1. Click **New repository secret** button
2. Name: `GOOGLE_CREDENTIALS_JSON`
3. Value: Contents of your `credentials.json` file as a single line
   
   **To convert credentials.json to single line:**
   
   On Windows (PowerShell):
   ```powershell
   (Get-Content -Path credentials.json -Raw) | ConvertFrom-Json | ConvertTo-Json -Compress
   ```
   
   On Mac/Linux:
   ```bash
   cat credentials.json | jq -c .
   ```
   
   Then copy the entire output and paste it into the secret value

4. Click **Add secret**

### Step 3: Verify Setup

After adding the secrets, you should see:
```
GOOGLE_CREDENTIALS_JSON
GOOGLE_SPREADSHEET_ID
```

Listed under "Repository secrets" (they'll show with a ⭐ icon).

## How the Workflow Uses the Secrets

When you push to `master`, the GitHub Actions workflow:

1. **Checks out your code** from the repository
2. **Creates `credentials.json`** from the secret using:
   ```yaml
   echo "${{ secrets.GOOGLE_CREDENTIALS_JSON }}" > credentials.json
   ```
3. **Sets environment variables** from secrets:
   ```yaml
   env:
     GOOGLE_SPREADSHEET_ID: ${{ secrets.GOOGLE_SPREADSHEET_ID }}
     GOOGLE_SHEET_NAME: Members
     GOOGLE_CREDENTIALS_PATH: credentials.json
   ```
4. **Runs `export_static.py`** which can now access:
   - `os.getenv("GOOGLE_SPREADSHEET_ID")` from secrets
   - The `credentials.json` file
5. **Generates static HTML** with the Google Sheet data
6. **Deploys to GitHub Pages** with the updated static site

## Security Best Practices

✅ **Do:**
- Store credentials as secrets
- Rotate credentials periodically
- Use service accounts (not personal accounts)
- Review who has access to your repo

❌ **Don't:**
- Commit `credentials.json` to Git (it's in `.gitignore`)
- Commit `.env` file to Git (it's in `.gitignore`)
- Share secrets in issues, PRs, or discussions
- Use personal API keys or passwords

## Troubleshooting

### Workflow shows error: "Credentials file not found"
- Verify you added `GOOGLE_CREDENTIALS_JSON` secret
- Check that the secret contains valid JSON
- Make sure the JSON is in single-line format

### "Invalid credentials"
- Verify the `credentials.json` content is correct
- Check that the service account has access to your Google Sheet
- Ensure the service account hasn't been deleted

### "Spreadsheet not found"
- Verify `GOOGLE_SPREADSHEET_ID` is correct
- Copy it from the URL bar (long alphanumeric string)
- Make sure it's exactly right with no extra spaces

### Workflow logs don't show secrets
- This is expected! GitHub automatically masks secrets in logs
- If you see `***` instead of the value, the secret is properly hidden

## Manual Testing Locally

To test locally with your credentials:
1. Create `.env` file (not committed):
   ```
   GOOGLE_SPREADSHEET_ID=your_id
   GOOGLE_CREDENTIALS_PATH=credentials.json
   GOOGLE_SHEET_NAME=Members
   ```
2. Place `credentials.json` in project root
3. Run: `python export_static.py`
4. Check `docs/index.html` was updated

Then delete both files before committing (they're in `.gitignore`).

## Next Steps

1. Add the two secrets to your GitHub repository
2. Commit any changes to the workflow
3. Push to `master` and watch the Actions tab for success
4. Check `https://elghouali.github.io/N7_Club_Kiosk/` for updated member count

The workflow will run automatically on every push to `master`!
