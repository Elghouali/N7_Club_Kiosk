from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from datetime import datetime
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# --- CONFIGURATION ---
EXCEL_FILE = "n7_club_members.xlsx"
AWS_LINK = "https://chat.whatsapp.com/DzEjjfEHm8E5FqU5ADNrJh"

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
    """Reads the Excel file to get current count."""
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE)
            return len(df)
        except:
            return 0
    return 0

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

    # Create Data Structure
    new_entry = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Full Name": [name],
        "Email": [email],
        "Phone": [phone],
        "Major": [major]
    }
    df_new = pd.DataFrame(new_entry)

    # Save to Excel safely
    try:
        if not os.path.exists(EXCEL_FILE):
            df_new.to_excel(EXCEL_FILE, index=False)
        else:
            # Append to existing file
            with pd.ExcelWriter(EXCEL_FILE, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                # Find the first empty row
                try:
                    reader = pd.read_excel(EXCEL_FILE, engine='openpyxl')
                    start_row = len(reader) + 1
                except pd.errors.EmptyDataError:
                    start_row = 1
                
                df_new.to_excel(writer, index=False, header=False, startrow=start_row)
                
        new_count = get_member_count()
        return jsonify({"status": "success", "new_count": new_count, "name": name})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    # host='0.0.0.0' makes it accessible on your local network if needed
    app.run(debug=True, port=5000)