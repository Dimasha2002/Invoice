from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

app = Flask(__name__)

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'invoices')
DATABASE_FILE = os.path.join(BASE_DIR, 'invoices_data.json')

def get_signature_path():
    """Return first available signature image path."""
    candidates = ['sign.jpeg', 'sign.jpg', 'sign.png']
    for name in candidates:
        path = os.path.join(BASE_DIR, name)
        if os.path.exists(path):
            return path
    return None

# Create invoices folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created invoices folder: {UPLOAD_FOLDER}")

def load_invoices():
    """Load invoices from JSON file"""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_invoices(invoices):
    """Save invoices to JSON file"""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(invoices, f, indent=2)

def get_next_invoice_id():
    """Get next invoice ID"""
    invoices = load_invoices()
    if not invoices:
        return 1
    return max([inv['id'] for inv in invoices]) + 1

def generate_pdf(invoice):
    """Generate PDF file for invoice with professional design"""
    try:
        pdf_filename = f"invoice_{invoice['id']}.pdf"
        pdf_file = os.path.join(UPLOAD_FOLDER, pdf_filename)
        
        print(f"Creating PDF at: {pdf_file}")
        
        doc = SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.3*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # ==================== HEADER == (Dark blue background)
        
        logo_path = os.path.join(BASE_DIR, 'logo.png')
        
        # Try to load logo
        logo_image = None
        try:
            if os.path.exists(logo_path):
                logo_image = Image(logo_path, width=1.2*inch, height=1.2*inch)
        except Exception as e:
            print(f"Logo error: {e}")
        
        # Header left: logo + company details
        company_title = Paragraph(
            "<b>Wedage Software Solutions</b>",
            ParagraphStyle('CompanyTitle', parent=styles['Normal'], fontSize=14, fontName='Helvetica-Bold', textColor=colors.white)
        )
        company_location = Paragraph(
            "Colombo, Sri Lanka",
            ParagraphStyle('CompanyInfo', parent=styles['Normal'], fontSize=9, textColor=colors.white)
        )
        company_email = Paragraph(
            "wedagesoftwaresolutions@gmail.com",
            ParagraphStyle('CompanyInfo', parent=styles['Normal'], fontSize=9, textColor=colors.white)
        )
        company_phone = Paragraph(
            "+94 76 139 0569",
            ParagraphStyle('CompanyInfo', parent=styles['Normal'], fontSize=9, textColor=colors.white)
        )
        
        company_details = Table([
            [company_title],
            [company_location],
            [company_email],
            [company_phone]
        ], colWidths=[2.2*inch])
        company_details.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        if logo_image:
            left_header = Table([[logo_image, company_details]], colWidths=[1.2*inch, 2.2*inch])
        else:
            left_header = Table([[company_details]], colWidths=[3.4*inch])
        
        left_header.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        # Header right: Invoice title + number + date
        right_header = Table([
            [Paragraph("Invoice", ParagraphStyle('HeaderTitle', parent=styles['Normal'], fontSize=28, fontName='Helvetica-Bold', textColor=colors.white, alignment=2))],
            [Paragraph(f"Invoice #INV-{invoice['id']:05d}", ParagraphStyle('HeaderMeta', parent=styles['Normal'], fontSize=9, textColor=colors.white, alignment=2))],
            [Paragraph(f"Date: {invoice['date']}", ParagraphStyle('HeaderMeta', parent=styles['Normal'], fontSize=9, textColor=colors.white, alignment=2))]
        ], colWidths=[3*inch])
        right_header.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (0, 0), 0),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        # Combine header
        full_header = Table([[left_header, right_header]], colWidths=[3.4*inch, 2.5*inch])
        full_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a56db')),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(full_header)
        
        # ==================== STATUS BANNER ====================
        
        if invoice['type'] == 'FULL' or (invoice['type'] == 'REST' and invoice['balance'] == 0):
            status_text = "✓ Fully Paid — No outstanding balance remaining"
            status_bg = colors.HexColor('#c8e6c9')
            status_color = colors.HexColor('#2e7d32')
        elif invoice['type'] == 'REST':
            status_text = "✓ Partially Paid — Awaiting final payment"
            status_bg = colors.HexColor('#b3e5fc')
            status_color = colors.HexColor('#0277bd')
        else:  # ADVANCE
            status_text = "⏳ Pending — Awaiting payment"
            status_bg = colors.HexColor('#ffe0b2')
            status_color = colors.HexColor('#f57c00')
        
        status_banner = Table([[Paragraph(f"<b>{status_text}</b>", ParagraphStyle('Status', parent=styles['Normal'], fontSize=10, textColor=status_color, fontName='Helvetica-Bold'))]], colWidths=[6*inch])
        status_banner.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), status_bg),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(status_banner)
        elements.append(Spacer(1, 0.15*inch))
        
        # ==================== BILL TO + BALANCE DUE (Side by side) ====================
        
        bill_to_label = ParagraphStyle('BillToLabel', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor('#1a5490'), spaceAfter=3)
        bill_to_name = ParagraphStyle('BillToName', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold', spaceAfter=3)
        bill_to_info = ParagraphStyle('BillToInfo', parent=styles['Normal'], fontSize=9, spaceAfter=1)
        
        bill_to = Table([
            [Paragraph("BILL TO", bill_to_label)],
            [Paragraph(invoice['customer_name'], bill_to_name)],
            [Paragraph(invoice['phone'], bill_to_info)],
            [Paragraph(invoice['description'], bill_to_info)]
        ], colWidths=[2.8*inch])
        bill_to.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e3f2fd')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor('#bbdefb')),
        ]))
        
        # Balance Due section
        balance_label = ParagraphStyle('BalanceLabel', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor('#1a5490'), alignment=2)
        balance_amount = ParagraphStyle('BalanceAmount', parent=styles['Normal'], fontSize=24, fontName='Helvetica-Bold', textColor=colors.HexColor('#2e7d32'), alignment=2, spaceAfter=2)
        balance_status = ParagraphStyle('BalanceStatus', parent=styles['Normal'], fontSize=8, fontName='Helvetica-Bold', textColor=colors.HexColor('#4caf50'), alignment=2, spaceAfter=6)
        balance_info = ParagraphStyle('BalanceInfo', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#666666'), alignment=2, spaceAfter=1)
        
        balance_due = Table([
            [Paragraph("BALANCE DUE", balance_label)],
            [Paragraph(f"${invoice['balance']:,.2f}", balance_amount)],
            [Paragraph("FULLY SETTLED" if invoice['balance'] == 0 else "PENDING", balance_status)],
            [Paragraph(f"Total invoiced: ${invoice['total_amount']:,.2f}", balance_info)],
            [Paragraph(f"Amount received: ${invoice['advance_paid']:,.2f}", balance_info)]
        ], colWidths=[2.8*inch])
        balance_due.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
        ]))
        
        # Side by side
        top_content = Table([[bill_to, balance_due]], colWidths=[2.9*inch, 2.9*inch])
        top_content.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(top_content)
        elements.append(Spacer(1, 0.2*inch))
        
        # ==================== ITEMS TABLE ====================
        
        if invoice['type'] == 'REST':
            item_headers = ["DESCRIPTION", "AMOUNT", "PAID", "BALANCE"]
            item_values = [
                invoice['description'],
                f"${invoice['total_amount']:,.2f}",
                f"${invoice['advance_paid']:,.2f}",
                f"${invoice.get('rest_amount', 0):,.2f}"
            ]
        else:
            item_headers = ["DESCRIPTION", "AMOUNT", "PAID", "BALANCE"]
            item_values = [
                invoice['description'],
                f"${invoice['total_amount']:,.2f}",
                f"${invoice['advance_paid']:,.2f}",
                f"${invoice['balance']:,.2f}"
            ]
        
        # Build header row
        header_cells = [Paragraph(f"<b>{h}</b>", ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.whitesmoke, fontSize=9)) for h in item_headers]
        
        # Build data row
        data_cells = [
            Paragraph(item_values[0], styles['Normal']),
            Paragraph(item_values[1], ParagraphStyle('Right', parent=styles['Normal'], alignment=2)),
            Paragraph(item_values[2], ParagraphStyle('RightGreen', parent=styles['Normal'], alignment=2, textColor=colors.HexColor('#2e7d32'), fontName='Helvetica-Bold')),
            Paragraph(item_values[3], ParagraphStyle('Right', parent=styles['Normal'], alignment=2))
        ]
        
        items_table = Table([header_cells, data_cells], colWidths=[2.2*inch, 1.3*inch, 1.3*inch, 1.3*inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (-1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('LEFTPADDING', (0, 0), (0, 0), 8),
            ('RIGHTPADDING', (1, 0), (-1, 0), 8),
            
            # Data row
            ('ALIGN', (0, 1), (0, 1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, 1), 'RIGHT'),
            ('VALIGN', (0, 1), (-1, 1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, 1), 9),
            ('TOPPADDING', (0, 1), (-1, 1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
            ('LEFTPADDING', (0, 1), (0, 1), 8),
            ('RIGHTPADDING', (1, 1), (-1, 1), 8),
            
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f9f9f9')),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # ==================== SUMMARY ====================
        
        summary_label = ParagraphStyle('SumLabel', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold', alignment=2, rightIndent=5)
        summary_value = ParagraphStyle('SumValue', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', alignment=2)
        summary_value_green = ParagraphStyle('SumGreen', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', alignment=2, textColor=colors.HexColor('#2e7d32'))
        
        summary_data = [
            [Paragraph("Subtotal", summary_label), Paragraph(f"${invoice['total_amount']:,.2f}", summary_value)],
            [Paragraph("Amount Paid", summary_label), Paragraph(f"${invoice['advance_paid']:,.2f}", summary_value_green)],
            [Paragraph("<b>BALANCE DUE</b>", ParagraphStyle('SumDueLabel', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', alignment=2, rightIndent=5)), Paragraph(f"<b>${invoice['balance']:,.2f}</b>", ParagraphStyle('SumDue', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', alignment=2))]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.whitesmoke),
            ('LINEABOVE', (0, 2), (-1, 2), 1, colors.HexColor('#dddddd')),
            ('TOPPADDING', (0, 2), (-1, 2), 10),
            ('BOTTOMPADDING', (0, 2), (-1, 2), 10),
        ]))
        
        # Right align summary
        summary_wrapper = Table([['', '', summary_table]], colWidths=[1.5*inch, 1.5*inch, 3.5*inch])
        summary_wrapper.setStyle(TableStyle([
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('VALIGN', (2, 0), (2, 0), 'TOP'),
            ('LEFTPADDING', (2, 0), (2, 0), 0),
            ('RIGHTPADDING', (2, 0), (2, 0), 0),
        ]))
        elements.append(summary_wrapper)
        elements.append(Spacer(1, 0.2*inch))
        
        # ==================== FOOTER ====================
        
        sign_path = get_signature_path()
        signature_image = None
        try:
            if sign_path:
                signature_image = Image(sign_path, width=2.0 * inch, height=0.65 * inch)
        except Exception as e:
            print(f"Signature error: {e}")

        issued_name = Paragraph(
            "<font size=10 color=#111111><b>Dimasha Hansani Abeywickrama</b></font>",
            ParagraphStyle('IssuedName', parent=styles['Normal'], alignment=1)
        )

        issued_role = Paragraph(
            "<font size=9><b>PROJECT MANAGER</b></font>",
            ParagraphStyle('IssuedRole', parent=styles['Normal'], alignment=1)
        )

        sign_line = Paragraph(
            "<font color=#bdbdbd>______________________________</font>",
            ParagraphStyle('SignLine', parent=styles['Normal'], alignment=1)
        )

        if signature_image:
            issued_section = Table([[signature_image], [sign_line], [issued_name], [issued_role]], colWidths=[2.6 * inch])
            issued_section.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (0, 0), -4),
                ('TOPPADDING', (0, 1), (0, 1), -2),
                ('TOPPADDING', (0, 2), (0, 2), 2),
            ]))
        else:
            issued_section = Table([[sign_line], [issued_name], [issued_role]], colWidths=[2.6 * inch])
            issued_section.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))

        issued_wrapper = Table([['', issued_section]], colWidths=[3.4 * inch, 2.6 * inch])
        issued_wrapper.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (1, 0), (1, 0), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(issued_wrapper)
        elements.append(Spacer(1, 0.12 * inch))

        footer_text = Paragraph(
            "Thank you for choosing Wedage Software Solutions.<br/>" +
            f"<font size=7>This invoice was issued on {invoice['date']} and reflects the payment status as shown above.</font>",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=0, spaceAfter=5)
        )
        elements.append(footer_text)
        
        # ==================== BUILD ====================
        
        doc.build(elements)
        print(f"PDF created successfully at: {pdf_file}")
        return pdf_file
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        raise

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/invoice/<int:invoice_id>')
def view_invoice(invoice_id):
    """View invoice detail page"""
    return render_template('invoice_detail.html')

@app.route('/logo.png')
def serve_logo():
    """Serve the logo file"""
    logo_path = os.path.join(BASE_DIR, 'logo.png')
    if os.path.exists(logo_path):
        return send_file(logo_path, mimetype='image/png')
    return 'Logo not found', 404

@app.route('/sign.jpeg')
def serve_sign():
    """Serve the signature image"""
    sign_path = get_signature_path()
    if sign_path:
        ext = os.path.splitext(sign_path)[1].lower()
        mime = 'image/png' if ext == '.png' else 'image/jpeg'
        return send_file(sign_path, mimetype=mime)
    return 'Signature not found', 404

@app.route('/paid.avif')
def serve_paid_badge():
    """Serve paid badge image for completed invoices"""
    paid_path = os.path.join(BASE_DIR, 'paid.avif')
    if os.path.exists(paid_path):
        return send_file(paid_path, mimetype='image/avif')
    return 'Paid badge not found', 404

@app.route('/paidmark.jpg')
def serve_paid_mark():
    """Serve paid mark image for completed invoices"""
    paid_path = os.path.join(BASE_DIR, 'paidmark.jpg')
    if os.path.exists(paid_path):
        return send_file(paid_path, mimetype='image/jpeg')
    return 'Paid mark not found', 404

@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    """Get all invoices"""
    invoices = load_invoices()
    # Add pdf_file field for each invoice
    for inv in invoices:
        inv['pdf_file'] = f"invoice_{inv['id']}.pdf"
    return jsonify(invoices)

@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    """Create new invoice"""
    data = request.json
    
    # Validation
    if not data.get('customer_name'):
        return jsonify({'error': 'Customer name is required'}), 400
    
    if not data.get('phone'):
        return jsonify({'error': 'Phone is required'}), 400
    
    if not data.get('description'):
        return jsonify({'error': 'Description is required'}), 400
    
    try:
        total_amount = float(data.get('total_amount', 0))
        advance_paid = float(data.get('advance_paid', 0))
    except:
        return jsonify({'error': 'Invalid amount values'}), 400
    
    if total_amount <= 0:
        return jsonify({'error': 'Total amount must be greater than 0'}), 400
    
    # Get payment type from request
    payment_type = data.get('payment_type', 'advance')
    
    # Validate based on payment type
    rest_amount = None
    if payment_type == 'advance':
        if advance_paid <= 0 or advance_paid >= total_amount:
            return jsonify({'error': 'For Advance, paid amount must be greater than 0 and less than total amount'}), 400
        balance = total_amount - advance_paid
        invoice_type = 'ADVANCE'
    elif payment_type == 'rest':
        # For REST: advance_paid is the already paid amount (advanced)
        if advance_paid <= 0 or advance_paid >= total_amount:
            return jsonify({'error': 'For Rest, advanced amount must be greater than 0 and less than total amount'}), 400
        rest_amount = total_amount - advance_paid
        balance = 0
        invoice_type = 'REST'
    elif payment_type == 'full':
        if advance_paid != total_amount:
            return jsonify({'error': 'For Full, paid amount must equal total amount'}), 400
        balance = 0
        invoice_type = 'FULL'
    else:
        return jsonify({'error': 'Invalid payment type'}), 400
    
    # Create invoice
    invoice = {
        'id': get_next_invoice_id(),
        'customer_name': data.get('customer_name'),
        'phone': data.get('phone'),
        'description': data.get('description'),
        'total_amount': total_amount,
        'advance_paid': advance_paid,
        'balance': balance,
        'rest_amount': rest_amount,
        'type': invoice_type,
        'payment_type_label': 'Advance' if invoice_type == 'ADVANCE' else ('Rest' if invoice_type == 'REST' else 'Full'),
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Generate PDF first
    try:
        pdf_filename = f"invoice_{invoice['id']}.pdf"
        generate_pdf(invoice)
        invoice['pdf_file'] = pdf_filename
    except Exception as e:
        return jsonify({'error': f'Error generating PDF: {str(e)}'}), 500
    
    # Save to database
    invoices = load_invoices()
    invoices.append(invoice)
    save_invoices(invoices)
    
    return jsonify(invoice), 201

@app.route('/api/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """Get specific invoice"""
    invoices = load_invoices()
    for invoice in invoices:
        if invoice['id'] == invoice_id:
            return jsonify(invoice)
    return jsonify({'error': 'Invoice not found'}), 404

@app.route('/download/<filename>')
def download_pdf(filename):
    """Download PDF file"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    print(f"Attempting to download: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
        print(f"File not found: {file_path}")
        return jsonify({'error': f'File not found: {filename}'}), 404

@app.route('/api/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    """Delete invoice"""
    invoices = load_invoices()
    invoices = [inv for inv in invoices if inv['id'] != invoice_id]
    save_invoices(invoices)
    
    # Delete PDF file
    pdf_file = os.path.join(UPLOAD_FOLDER, f"invoice_{invoice_id}.pdf")
    if os.path.exists(pdf_file):
        os.remove(pdf_file)
    
    return jsonify({'message': 'Invoice deleted successfully'}), 200

if __name__ == '__main__':
    print("Starting Invoice Generator Web Application...")
    print("Open your browser and go to: http://localhost:8000")
    app.run(debug=True, port=8000)
