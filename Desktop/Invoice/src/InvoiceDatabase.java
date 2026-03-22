import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class InvoiceDatabase {
    private static final String DB_FILE = "invoices.dat";
    
    public static void saveInvoice(Invoice invoice) {
        try {
            List<Invoice> invoices = loadAllInvoices();
            invoices.add(invoice);
            
            FileOutputStream fos = new FileOutputStream(DB_FILE);
            ObjectOutputStream oos = new ObjectOutputStream(fos);
            oos.writeObject(invoices);
            oos.close();
            fos.close();
            
            System.out.println("Invoice saved to database: " + invoice.getInvoiceId());
        } catch (IOException e) {
            System.out.println("Error saving invoice: " + e.getMessage());
        }
    }
    
    public static List<Invoice> loadAllInvoices() {
        try {
            File file = new File(DB_FILE);
            if (file.exists()) {
                FileInputStream fis = new FileInputStream(DB_FILE);
                ObjectInputStream ois = new ObjectInputStream(fis);
                @SuppressWarnings("unchecked")
                List<Invoice> invoices = (List<Invoice>) ois.readObject();
                ois.close();
                fis.close();
                return invoices;
            }
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Error loading invoices: " + e.getMessage());
        }
        return new ArrayList<>();
    }
    
    public static Invoice getInvoiceById(int id) {
        List<Invoice> invoices = loadAllInvoices();
        for (Invoice invoice : invoices) {
            if (invoice.getInvoiceId() == id) {
                return invoice;
            }
        }
        return null;
    }
    
    public static int getLastInvoiceId() {
        List<Invoice> invoices = loadAllInvoices();
        if (invoices.isEmpty()) {
            return 0;
        }
        return invoices.get(invoices.size() - 1).getInvoiceId();
    }
    
    public static void deleteDatabase() {
        File file = new File(DB_FILE);
        if (file.exists()) {
            file.delete();
        }
    }
}
