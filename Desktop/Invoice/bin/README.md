# Invoice Generator - Java Swing Application

## Installation

### 1. JAR Files (Already Added)
✅ iText7-Core-7.2.0 library is in the `iText7-Core-7.2.0` folder

### 2. How to Run

**Option A: Double-click `run.bat`** (Easiest)
- Directly launches the application
- Use this after first compilation

**Option B: Double-click `compile_and_run.bat`**
- Compiles the project first
- Then launches the application
- Use this if you made code changes

**Option C: Manual command in PowerShell**
```powershell
cd C:\Users\USER\Desktop\Invoice\src
java -cp "iText7-Core-7.2.0\kernel-7.2.0.jar;iText7-Core-7.2.0\io-7.2.0.jar;iText7-Core-7.2.0\layout-7.2.0.jar;iText7-Core-7.2.0\commons-7.2.0.jar;." InvoiceForm
```

## Features

✅ **Create Invoices**
- Enter customer name, phone, description
- Enter total amount and advance paid
- Click "Generate Invoice"
- Real PDF file created instantly

✅ **View All Invoices**
- Click "View Invoices" button
- See all previously created invoices
- View invoice details

✅ **Open PDF**
- Click "Open PDF" button
- Select an invoice from the list
- Opens in your default PDF reader

✅ **Automatic Database**
- All invoices saved to `invoices.dat`
- Data persists between sessions
- Auto-increment invoice IDs

## File Structure

```
Invoice/
├── src/
│   ├── Invoice.java
│   ├── InvoiceService.java
│   ├── InvoiceDatabase.java
│   ├── PDFGenerator.java
│   ├── InvoiceForm.java
│   ├── Main.java
│   ├── iText7-Core-7.2.0/        (JAR libraries)
│   ├── run.bat                     (Quick start)
│   ├── compile_and_run.bat         (Compile & start)
│   └── invoices.dat                (Database file)
```

## Generated Files

- `invoice_1.pdf` - First invoice
- `invoice_2.pdf` - Second invoice
- `invoices.dat` - Database with all invoice data

## Troubleshooting

**If you get a "class not found" error:**
- Make sure you're in the `src` folder
- Check that JAR files are in `iText7-Core-7.2.0` folder
- Use `compile_and_run.bat` instead of `run.bat`

**If PDFs don't open:**
- Check if they exist in the src folder
- Make sure you have a PDF reader installed (Adobe Reader, etc.)

---

**Happy Invoice Generating!** 🎉
