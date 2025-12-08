from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import qrcode
from io import BytesIO
import base64
from dotenv import load_dotenv
from google_sheets_client import init_google_sheets, add_member, get_member_count

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --- CONFIGURATION ---
AWS_LINK = "https://chat.whatsapp.com/DzEjjfEHm8E5FqU5ADNrJh"
SPREADSHEET_ID = os.getenv("GOOGLE_SPREADSHEET_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Members")
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")

# Initialize Google Sheets client on startup
try:
    if not CREDENTIALS_JSON:
        raise Exception("GOOGLE_CREDENTIALS_JSON environment variable not set")
    if not SPREADSHEET_ID:
        raise Exception("GOOGLE_SPREADSHEET_ID environment variable not set")
    
    init_google_sheets(SPREADSHEET_ID, SHEET_NAME, CREDENTIALS_JSON)
    SHEETS_INITIALIZED = True
except Exception as e:
    print(f"Warning: Could not initialize Google Sheets: {e}")
    print("The app will still run, but member data won't be saved.")
    SHEETS_INITIALIZED = False

# --- HELPER FUNCTIONS ---
def generate_qr_base64(link):
    """Generates a QR code and converts it to a base64 string for HTML."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(link)
    qr.make(fit=True)
    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_member_count():
    """Get current count from Google Sheets."""
    if not SHEETS_INITIALIZED:
        return 0
    try:
        return get_member_count_from_sheets()
    except:
        return 0

# Import the actual function with a different name to avoid recursion
from google_sheets_client import get_member_count as get_member_count_from_sheets

# --- ROUTES ---
@app.route('/')
def home():
    count = get_member_count()
    # We generate the QR code once when the page loads
    qr_code_data = generate_qr_base64(AWS_LINK)
    return render_template('index.html', count=count, qr_code=qr_code_data)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    major = data.get('major')

    if not name or not email:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    if not SHEETS_INITIALIZED:
        return jsonify({"status": "error", "message": "Google Sheets not configured. Please add credentials.json and .env file."}), 500

    # Save to Google Sheets
    try:
        add_member(name, email, phone, major)
        new_count = get_member_count_from_sheets()
        return jsonify({"status": "success", "new_count": new_count, "name": name})
    except Exception as e:
        print(f"Error adding member: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    # host='0.0.0.0' makes it accessible on your local network if needed
    app.run(debug=True, port=5000)