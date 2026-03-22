import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Paragraph;
import com.itextpdf.layout.properties.TextAlignment;
import java.io.File;
import java.awt.Desktop;

public class PDFGenerator {
    
    public static void generatePDF(Invoice invoice) {
        if (invoice == null) {
            System.out.println("Error: Invoice is null. Cannot generate PDF.");
            return;
        }
        
        try {
            String fileName = "invoice_" + invoice.getInvoiceId() + ".pdf";
            
            // Create PDF
            PdfWriter writer = new PdfWriter(fileName);
            PdfDocument pdfDoc = new PdfDocument(writer);
            Document document = new Document(pdfDoc);
            
            // Title
            Paragraph title = new Paragraph("INVOICE")
                    .setTextAlignment(TextAlignment.CENTER)
                    .setFontSize(24)
                    .setBold();
            document.add(title);
            
            // Separator
            document.add(new Paragraph("========================================"));
            
            // Invoice ID and Date
            document.add(new Paragraph("Invoice ID: " + invoice.getInvoiceId())
                    .setFontSize(11));
            document.add(new Paragraph("Date: " + invoice.getDate())
                    .setFontSize(11));
            
            // Customer Details
            document.add(new Paragraph("\nCUSTOMER DETAILS")
                    .setFontSize(12)
                    .setBold());
            document.add(new Paragraph("Name: " + invoice.getCustomerName())
                    .setFontSize(11));
            document.add(new Paragraph("Phone: " + invoice.getPhone())
                    .setFontSize(11));
            
            // Description
            document.add(new Paragraph("\nDESCRIPTION")
                    .setFontSize(12)
                    .setBold());
            document.add(new Paragraph(invoice.getDescription())
                    .setFontSize(11));
            
            // Payment Details
            document.add(new Paragraph("\nPAYMENT DETAILS")
                    .setFontSize(12)
                    .setBold());
            document.add(new Paragraph("Total Amount: $" + String.format("%.2f", invoice.getTotalAmount()))
                    .setFontSize(11));
            document.add(new Paragraph("Advance Paid: $" + String.format("%.2f", invoice.getAdvancePaid()))
                    .setFontSize(11));
            document.add(new Paragraph("Balance: $" + String.format("%.2f", invoice.getBalance()))
                    .setFontSize(11));
            
            // Invoice Type
            document.add(new Paragraph("\nInvoice Type: " + invoice.getType())
                    .setFontSize(12)
                    .setBold());
            
            // Separator
            document.add(new Paragraph("\n========================================"));
            document.add(new Paragraph("Thank you for your business!")
                    .setTextAlignment(TextAlignment.CENTER)
                    .setFontSize(11));
            document.add(new Paragraph("========================================")
                    .setTextAlignment(TextAlignment.CENTER));
            
            document.close();
            System.out.println("PDF created successfully: " + fileName);
            
        } catch (Exception e) {
            System.out.println("Error creating PDF: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    public static void openPDF(String fileName) {
        try {
            File file = new File(fileName);
            if (file.exists()) {
                Desktop.getDesktop().open(file);
                System.out.println("Opening file: " + fileName);
            } else {
                System.out.println("File not found: " + fileName);
            }
        } catch (Exception e) {
            System.out.println("Error opening file: " + e.getMessage());
        }
    }
}



