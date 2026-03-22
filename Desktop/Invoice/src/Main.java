import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        InvoiceService service = new InvoiceService();
        
        System.out.println("===== Invoice Generator =====\n");
        
        try {
            // Get customer name
            System.out.print("Enter Customer Name: ");
            String customerName = scanner.nextLine().trim();
            
            if (customerName.isEmpty()) {
                System.out.println("Error: Customer name cannot be empty.");
                return;
            }
            
            // Get phone
            System.out.print("Enter Phone Number: ");
            String phone = scanner.nextLine().trim();
            
            if (phone.isEmpty()) {
                System.out.println("Error: Phone number cannot be empty.");
                return;
            }
            
            // Get description
            System.out.print("Enter Description: ");
            String description = scanner.nextLine().trim();
            
            if (description.isEmpty()) {
                System.out.println("Error: Description cannot be empty.");
                return;
            }
            
            // Get total amount
            System.out.print("Enter Total Amount: $");
            double totalAmount = getDoubleInput(scanner);
            
            // Get advance paid
            System.out.print("Enter Advance Paid: $");
            double advancePaid = getDoubleInput(scanner);
            
            System.out.println();
            
            // Create invoice
            Invoice invoice = service.createInvoice(customerName, phone, description, 
                                                     totalAmount, advancePaid);
            
            // Check if invoice is valid
            if (invoice == null) {
                System.out.println("Failed to create invoice. Please check your inputs.");
                return;
            }
            
            // Display invoice details
            System.out.println("\n" + invoice);
            
            // Generate PDF
            System.out.println("\nGenerating PDF...");
            PDFGenerator.generatePDF(invoice);
            
            System.out.println("\n✓ Invoice created successfully!");
            
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            scanner.close();
        }
    }
    
    // Helper method to get double input with validation
    private static double getDoubleInput(Scanner scanner) {
        while (true) {
            try {
                String input = scanner.nextLine().trim();
                return Double.parseDouble(input);
            } catch (NumberFormatException e) {
                System.out.print("Invalid input. Please enter a valid number: ");
            }
        }
    }
}
