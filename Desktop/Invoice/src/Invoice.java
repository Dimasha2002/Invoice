import java.io.Serializable;

public class Invoice implements Serializable {
    private static final long serialVersionUID = 1L;
    
    public static final String ADVANCE = "ADVANCE";
    public static final String FINAL = "FINAL";
    
    private int invoiceId;
    private String customerName;
    private String phone;
    private String description;
    private double totalAmount;
    private double advancePaid;
    private double balance;
    private String type;
    private String date;
    
    public Invoice(int invoiceId, String customerName, String phone, String description,
                   double totalAmount, double advancePaid, String type, String date) {
        this.invoiceId = invoiceId;
        this.customerName = customerName;
        this.phone = phone;
        this.description = description;
        this.totalAmount = totalAmount;
        this.advancePaid = advancePaid;
        this.balance = totalAmount - advancePaid;
        this.type = type;
        this.date = date;
    }
    
    public int getInvoiceId() {
        return invoiceId;
    }
    
    public String getCustomerName() {
        return customerName;
    }
    
    public String getPhone() {
        return phone;
    }
    
    public String getDescription() {
        return description;
    }
    
    public double getTotalAmount() {
        return totalAmount;
    }
    
    public double getAdvancePaid() {
        return advancePaid;
    }
    
    public double getBalance() {
        return balance;
    }
    
    public String getType() {
        return type;
    }
    
    public String getDate() {
        return date;
    }
    
    public void setAdvancePaid(double advancePaid) {
        this.advancePaid = advancePaid;
        this.balance = totalAmount - advancePaid;
    }
    
    @Override
    public String toString() {
        return "Invoice{" +
                "invoiceId=" + invoiceId +
                ", customerName='" + customerName + '\'' +
                ", phone='" + phone + '\'' +
                ", description='" + description + '\'' +
                ", totalAmount=" + totalAmount +
                ", advancePaid=" + advancePaid +
                ", balance=" + balance +
                ", type='" + type + '\'' +
                ", date='" + date + '\'' +
                '}';
    }
}
