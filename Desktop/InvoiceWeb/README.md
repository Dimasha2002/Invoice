# Invoice Generator - Web Application

A simple and elegant web-based invoice generator built with Python Flask.

## Features

✅ **Create Invoices**
- Fill in customer details
- Enter amount and advance paid
- Automatic invoice ID generation
- Automatic balance calculation
- Type detection (ADVANCE/FINAL)

✅ **Real PDF Generation**
- Professional PDF invoices
- Download anytime
- Auto-saved invoices

✅ **Manage Invoices**
- View all created invoices
- Download PDF anytime
- Delete invoices
- Persistent database

✅ **Beautiful UI**
- Modern responsive design
- Works on desktop and mobile
- Real-time updates
- Smooth animations

## Installation & Setup

### 1. Install Python (if not installed)
Download from: https://www.python.org/downloads/
Make sure to check "Add Python to PATH"

### 2. Install Dependencies
```bash
pip install Flask reportlab
```

Or use the batch file:
```
Double-click: run.bat
```

### 3. Run the Application
```bash
python app.py
```

Or:
```
Double-click: run.bat
```

The app will open automatically at: **http://localhost:8000**

## Usage

1. **Fill the Form**
   - Customer Name
   - Phone
   - Description
   - Total Amount
   - Advance Paid

2. **Click "Generate Invoice"**
   - PDF is created immediately
   - Invoice saved to database
   - Shown in the list on right

3. **Download or Delete**
   - Click "Download PDF" to get the invoice
   - Click "Delete" to remove from database

## File Structure

```
InvoiceWeb/
├── app.py                 (Flask server)
├── requirements.txt       (Dependencies)
├── run.bat               (Run script)
├── README.md             (This file)
├── templates/
│   └── index.html        (Web UI)
├── invoices/             (Generated PDFs)
└── invoices_data.json    (Database)
```

## Database

Invoices are stored in `invoices_data.json`
Format:
```json
[
  {
    "id": 1,
    "customer_name": "John Doe",
    "phone": "555-1234",
    "description": "Service",
    "total_amount": 1000.00,
    "advance_paid": 500.00,
    "balance": 500.00,
    "type": "ADVANCE",
    "date": "2026-03-21"
  }
]
```

## Troubleshooting

**Port already in use:**
```
Change port number in app.py:
app.run(debug=True, port=8001)  # Change 8000 to different number
```

**Module not found:**
```
pip install -r requirements.txt
```

**Can't download PDFs:**
- Check if PDFs exist in `invoices/` folder
- Try refreshing the browser

---

**Enjoy creating invoices!** 🎉
