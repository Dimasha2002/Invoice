import java.util.List;
import java.time.LocalDate;

public class InvoiceService {
    private List<Invoice> invoices;
    private int invoiceCounter;
    
    public InvoiceService() {
        this.invoices = InvoiceDatabase.loadAllInvoices();
        
        // Set counter to next ID after last invoice
        if (invoices.isEmpty()) {
            this.invoiceCounter = 1;
        } else {
            this.invoiceCounter = invoices.get(invoices.size() - 1).getInvoiceId() + 1;
        }
    }
    
    public Invoice createInvoice(String name, String phone, String description,
                                 double totalAmount, double advancePaid) {
        // Validation
        if (totalAmount <= 0) {
            System.out.println("Error: Total amount must be greater than 0");
            return null;
        }
        
        if (advancePaid < 0 || advancePaid > totalAmount) {
            System.out.println("Error: Advance paid must be between 0 and total amount");
            return null;
        }
        
        // Calculate balance and determine type
        double balance = totalAmount - advancePaid;
        String type;
        
        if (balance > 0) {
            type = Invoice.ADVANCE;
        } else {
            type = Invoice.FINAL;
        }
        
        // Generate invoice ID
        String invoiceId = "INV-" + String.format("%03d", invoiceCounter++);
        
        // Get current date
        String date = LocalDate.now().toString();
        
        // Create and add invoice
        Invoice invoice = new Invoice(Integer.parseInt(invoiceId.substring(4)),
                                      name, phone, description, 
                                      totalAmount, advancePaid, type, date);
        
        invoices.add(invoice);
        InvoiceDatabase.saveInvoice(invoice);
        System.out.println("Invoice created: " + invoiceId + " for " + name);
        return invoice;
    }
    
    public Invoice getInvoice(int id) {
        for (Invoice invoice : invoices) {
            if (invoice.getInvoiceId() == id) {
                return invoice;
            }
        }
        return null;
    }
    
    public List<Invoice> getAllInvoices() {
        return invoices;
    }
    
    public double getTotalAmount() {
        double total = 0;
        for (Invoice invoice : invoices) {
            total += invoice.getTotalAmount();
        }
        return total;
    }
    
    public void displayAllInvoices() {
        System.out.println("\n--- All Invoices ---");
        for (Invoice invoice : invoices) {
            System.out.println(invoice);
        }
        System.out.println("Total Amount: $" + getTotalAmount());
    }
}
