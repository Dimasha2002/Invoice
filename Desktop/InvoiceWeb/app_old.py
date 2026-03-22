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
    """Generate PDF file for invoice with professional, beautiful design"""
    try:
        pdf_filename = f"invoice_{invoice['id']}.pdf"
        pdf_file = os.path.join(UPLOAD_FOLDER, pdf_filename)
        
        print(f"Creating PDF at: {pdf_file}")
        
        doc = SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.4*inch, bottomMargin=1*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # ==================== HEADER WITH LOGO ====================
        
        logo_path = os.path.join(BASE_DIR, 'logo.png')
        
        if os.path.exists(logo_path):
            try:
                img = Image(logo_path, width=1*inch, height=1*inch)
                company_info = Paragraph(
                    "<font size=16><b>Wedage Software Solutions</b></font><br/>"
                    "<font size=10>Colombo, Sri Lanka</font><br/>"
                    "<font size=9>📧 info@wedage.com | 📞 +94 76 139 0569 / +94 71 775 4075</font>",
                    styles['Normal']
                )
                
                header_table_data = [[img, company_info]]
                header_table = Table(header_table_data, colWidths=[1.2*inch, 5.8*inch])
                header_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(header_table)
            except Exception as e:
                print(f"Logo error: {e}")
                elements.append(Paragraph(
                    "<font size=16><b>Wedage Software Solutions</b></font><br/>"
                    "<font size=10>Colombo, Sri Lanka | +94 76 139 0569 / +94 71 775 4075</font>",
                    styles['Normal']
                ))
        else:
            elements.append(Paragraph(
                "<font size=16><b>Wedage Software Solutions</b></font><br/>"
                "<font size=10>Colombo, Sri Lanka | +94 76 139 0569 / +94 71 775 4075</font>",
                styles['Normal']
            ))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # ==================== DECORATIVE HEADER LINE ====================
        
        line_table = Table([['▬' * 130]], colWidths=[7*inch])
        line_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1a5490')),
            ('FONTSIZE', (0, 0), (0, 0), 11),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 0),
            ('TOPPADDING', (0, 0), (0, 0), 5),
            ('BOTTOMPADDING', (0, 0), (0, 0), 5),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ==================== INVOICE TITLE AND DETAILS ====================
        
        title_table_data = [
            [
                Paragraph("<font size=40><b>INVOICE</b></font>", ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, textColor=colors.HexColor('#1a5490'), fontName='Helvetica-Bold')),
            ]
        ]
        
        title_table = Table(title_table_data, colWidths=[7*inch])
        title_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 0),
            ('TOPPADDING', (0, 0), (0, 0), 10),
            ('BOTTOMPADDING', (0, 0), (0, 0), 10),
        ]))
        elements.append(title_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Invoice meta info
        status = "Pending" if invoice['type'] == 'ADVANCE' else "Completed"
        status_color = colors.HexColor('#ff9800') if invoice['type'] == 'ADVANCE' else colors.HexColor('#4caf50')
        
        invoice_meta_data = [
            [
                Paragraph(f"<b>Invoice #:</b> <font color={colors.HexColor('#1a5490')}><b>INV-{invoice['id']:03d}</b></font>", styles['Normal']),
                Paragraph(f"<b>Date:</b> {invoice['date']}", styles['Normal']),
                Paragraph(f"<b>Status:</b> <font color={status_color}><b>● {status}</b></font>", styles['Normal'])
            ]
        ]
        
        invoice_meta_table = Table(invoice_meta_data, colWidths=[2.3*inch, 2.3*inch, 2.1*inch])
        invoice_meta_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(invoice_meta_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # ==================== BILL TO SECTION ====================
        
        bill_to_style = ParagraphStyle(
            'BillToHeader',
            parent=styles['Heading2'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=8
        )
        
        elements.append(Paragraph("BILL TO", bill_to_style))
        
        customer_data = [
            [Paragraph(f"<b>{invoice['customer_name']}</b>", styles['Normal'])],
            [Paragraph(f"Phone: {invoice['phone']}", styles['Normal'])],
            [Paragraph(f"Details: {invoice['description']}", styles['Normal'])]
        ]
        
        customer_table = Table(customer_data, colWidths=[6.5*inch])
        customer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f4f8')),
            ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor('#d0d0d0')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f0f4f8')]),
        ]))
        elements.append(customer_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # ==================== ITEMIZED TABLE ====================
        
        elements.append(Paragraph("INVOICE DETAILS", bill_to_style))
        
        item_data = [
            [
                Paragraph("<b>Description</b>", styles['Normal']),
                Paragraph("<b>Total Amount</b>", styles['Normal']),
                Paragraph("<b>Advance Paid</b>", styles['Normal']),
                Paragraph("<b>Balance</b>", styles['Normal'])
            ],
            [
                Paragraph(invoice['description'][:50], styles['Normal']),
                Paragraph(f"<b>${invoice['total_amount']:.2f}</b>", styles['Normal']),
                Paragraph(f"${invoice['advance_paid']:.2f}", styles['Normal']),
                Paragraph(f"<b>${invoice['balance']:.2f}</b>", styles['Normal'])
            ]
        ]
        
        item_table = Table(item_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        item_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            
            # Data
            ('ALIGN', (1, 1), (-1, 1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, 1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, 1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, 1), 10),
            ('TOPPADDING', (0, 1), (-1, 1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 10),
            ('LEFTPADDING', (0, 1), (-1, 1), 8),
            ('RIGHTPADDING', (0, 1), (-1, 1), 8),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f9f9f9')),
        ]))
        elements.append(item_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # ==================== SUMMARY SECTION ====================
        
        summary_data = [
            [
                Paragraph("<b>Subtotal</b>", ParagraphStyle('SummaryLabel', parent=styles['Normal'], fontName='Helvetica-Bold', alignment=2)),
                Paragraph(f"${invoice['total_amount']:.2f}", ParagraphStyle('SummaryValue', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', alignment=2))
            ],
            [
                Paragraph("<b>Paid Amount</b>", ParagraphStyle('SummaryLabel', parent=styles['Normal'], fontName='Helvetica-Bold', alignment=2)),
                Paragraph(f"${invoice['advance_paid']:.2f}", ParagraphStyle('SummaryValue', parent=styles['Normal'], alignment=2))
            ],
            [
                Paragraph("<b>BALANCE DUE</b>", ParagraphStyle('SummaryLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, alignment=2, textColor=colors.HexColor('#d32f2f'))),
                Paragraph(f"<b>${invoice['balance']:.2f}</b>", ParagraphStyle('SummaryValue', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold', alignment=2, textColor=colors.HexColor('#d32f2f')))
            ]
        ]
        
        summary_table = Table(summary_data, colWidths=[3.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (1, 0), (1, -1), 15),
            
            # Highlight last row
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#ffebee')),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.HexColor('#d32f2f')),
            ('LINEBELOW', (0, 2), (-1, 2), 2, colors.HexColor('#d32f2f')),
        ]))
        
        # Center the summary table
        summary_wrapper = Table([['', summary_table]], colWidths=[3.5*inch, 3.5*inch])
        summary_wrapper.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (1, 0), (1, 0), 'TOP'),
        ]))
        elements.append(summary_wrapper)
        
        elements.append(Spacer(1, 0.4*inch))
        
        # ==================== SIGNATURE SECTION ====================
        
        sig_line_style = ParagraphStyle(
            'SigLine',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#999999')
        )
        
        signature_data = [
            [
                Paragraph("Authorized By", ParagraphStyle('SigHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9)),
                Paragraph("Date", ParagraphStyle('SigHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9))
            ],
            [
                Paragraph("_________________", sig_line_style),
                Paragraph("_________________", sig_line_style)
            ]
        ]
        
        signature_table = Table(signature_data, colWidths=[3*inch, 2*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(signature_table)
        
        elements.append(Spacer(1, 0.15*inch))
        
        # ==================== FOOTER ====================
        
        footer_line_table = Table([['▬' * 130]], colWidths=[7*inch])
        footer_line_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1a5490')),
            ('FONTSIZE', (0, 0), (0, 0), 11),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 0),
            ('TOPPADDING', (0, 0), (0, 0), 5),
            ('BOTTOMPADDING', (0, 0), (0, 0), 5),
        ]))
        elements.append(footer_line_table)
        
        elements.append(Spacer(1, 0.08*inch))
        
        footer_text_style = ParagraphStyle(
            'FooterText',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1a5490'),
            alignment=1,
            spaceAfter=2
        )
        
        footer_small_style = ParagraphStyle(
            'FooterSmall',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#999999'),
            alignment=1
        )
        
        elements.append(Paragraph("Thank you for your business!", footer_text_style))
        elements.append(Paragraph("Wedage Software Solutions © 2026 | www.wedage.com", footer_small_style))
        
        doc.build(elements)
        print(f"PDF created successfully at: {pdf_file}")
        print(f"File exists: {os.path.exists(pdf_file)}")
        return pdf_file
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        raise

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

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
    
    if advance_paid < 0 or advance_paid > total_amount:
        return jsonify({'error': 'Advance paid must be between 0 and total amount'}), 400
    
    # Auto-calculate type based on balance
    balance = total_amount - advance_paid
    invoice_type = 'FINAL' if balance == 0 else 'ADVANCE'
    
    # Create invoice
    invoice = {
        'id': get_next_invoice_id(),
        'customer_name': data.get('customer_name'),
        'phone': data.get('phone'),
        'description': data.get('description'),
        'total_amount': total_amount,
        'advance_paid': advance_paid,
        'balance': balance,
        'type': invoice_type,
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
