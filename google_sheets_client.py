"""
Google Sheets integration for N7 Club Kiosk.
Handles reading and writing member data to Google Sheets.
"""

from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime

# Global sheet service instance
_sheets_service = None
_spreadsheet_id = None
_sheet_name = None

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def init_google_sheets(spreadsheet_id, sheet_name, credentials_path):
    """
    Initialize Google Sheets service with credentials.
    
    Args:
        spreadsheet_id: The Google Sheets spreadsheet ID
        sheet_name: The name of the sheet/tab to use
        credentials_path: Path to the service account credentials JSON file
    """
    global _sheets_service, _spreadsheet_id, _sheet_name
    
    try:
        credentials = Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES
        )
        _sheets_service = build('sheets', 'v4', credentials=credentials)
        _spreadsheet_id = spreadsheet_id
        _sheet_name = sheet_name
        print(f"✓ Google Sheets initialized: {sheet_name}")
        return True
    except FileNotFoundError:
        raise Exception(f"Credentials file not found: {credentials_path}")
    except Exception as e:
        raise Exception(f"Failed to initialize Google Sheets: {str(e)}")

def _get_sheet_service():
    """Get the sheets service, raise error if not initialized."""
    if _sheets_service is None:
        raise Exception("Google Sheets not initialized. Call init_google_sheets() first.")
    return _sheets_service

def _ensure_headers():
    """Ensure the sheet has headers in the first row."""
    service = _get_sheet_service()
    headers = ["Timestamp", "Full Name", "Email", "Phone", "Major"]
    
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=_spreadsheet_id,
            range=f"{_sheet_name}!A1:E1"
        ).execute()
        
        existing_values = result.get('values', [])
        
        # If no headers exist, add them
        if not existing_values or existing_values[0] != headers:
            service.spreadsheets().values().update(
                spreadsheetId=_spreadsheet_id,
                range=f"{_sheet_name}!A1:E1",
                valueInputOption="RAW",
                body={"values": [headers]}
            ).execute()
            print("✓ Headers created in Google Sheet")
    except Exception as e:
        print(f"Warning: Could not ensure headers: {e}")

def add_member(name, email, phone, major):
    """
    Add a new member to the Google Sheet.
    
    Args:
        name: Full name
        email: Email address
        phone: Phone number
        major: Major/Program
    
    Returns:
        dict: Updated member count and status
    """
    service = _get_sheet_service()
    
    try:
        # Ensure headers exist first
        _ensure_headers()
        
        # Prepare the data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = [[timestamp, name, email, phone or "", major or ""]]
        
        # Find the first empty row
        result = service.spreadsheets().values().get(
            spreadsheetId=_spreadsheet_id,
            range=f"{_sheet_name}!A:A"
        ).execute()
        
        values_list = result.get('values', [])
        next_row = len(values_list) + 1
        
        # Append the new member
        service.spreadsheets().values().append(
            spreadsheetId=_spreadsheet_id,
            range=f"{_sheet_name}!A{next_row}",
            valueInputOption="RAW",
            body={"values": values}
        ).execute()
        
        print(f"✓ Member added: {name} ({email})")
        return {"status": "success", "name": name}
        
    except Exception as e:
        raise Exception(f"Failed to add member: {str(e)}")

def get_member_count():
    """
    Get the total count of members in the Google Sheet.
    
    Returns:
        int: Number of members (excluding header row)
    """
    service = _get_sheet_service()
    
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=_spreadsheet_id,
            range=f"{_sheet_name}!A:A"
        ).execute()
        
        values = result.get('values', [])
        # Subtract 1 for the header row
        count = max(0, len(values) - 1)
        return count
        
    except Exception as e:
        print(f"Warning: Could not get member count: {e}")
        return 0

def get_all_members():
    """
    Get all members from the Google Sheet.
    
    Returns:
        list: List of member dictionaries
    """
    service = _get_sheet_service()
    
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=_spreadsheet_id,
            range=f"{_sheet_name}!A:E"
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            return []
        
        # Extract headers and data
        headers = values[0] if values else []
        members = []
        
        for row in values[1:]:  # Skip header
            if len(row) >= len(headers):
                member = dict(zip(headers, row))
                members.append(member)
        
        return members
        
    except Exception as e:
        print(f"Warning: Could not get members: {e}")
        return []
