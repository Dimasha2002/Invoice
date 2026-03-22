import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;

public class InvoiceForm extends JFrame {
    private JTextField nameField;
    private JTextField phoneField;
    private JTextArea descriptionArea;
    private JTextField totalAmountField;
    private JTextField advancePaidField;
    private JButton generateButton;
    private JButton viewInvoicesButton;
    private JButton openPDFButton;
    private InvoiceService service;
    
    public InvoiceForm() {
        service = new InvoiceService();
        
        // Frame settings
        setTitle("Invoice Generator");
        setSize(600, 650);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setResizable(false);
        
        // Create main panel
        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new BorderLayout());
        mainPanel.setBackground(new Color(240, 240, 240));
        
        // Title panel
        JPanel titlePanel = new JPanel();
        titlePanel.setBackground(new Color(70, 130, 180));
        JLabel titleLabel = new JLabel("Invoice Generator");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);
        titlePanel.add(titleLabel);
        mainPanel.add(titlePanel, BorderLayout.NORTH);
        
        // Form panel
        JPanel formPanel = new JPanel();
        formPanel.setLayout(new GridLayout(6, 2, 10, 15));
        formPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        formPanel.setBackground(new Color(240, 240, 240));
        
        // Customer Name
        formPanel.add(createLabel("Customer Name:"));
        nameField = new JTextField();
        nameField.setFont(new Font("Arial", Font.PLAIN, 12));
        formPanel.add(nameField);
        
        // Phone
        formPanel.add(createLabel("Phone:"));
        phoneField = new JTextField();
        phoneField.setFont(new Font("Arial", Font.PLAIN, 12));
        formPanel.add(phoneField);
        
        // Description
        formPanel.add(createLabel("Description:"));
        descriptionArea = new JTextArea(3, 20);
        descriptionArea.setFont(new Font("Arial", Font.PLAIN, 12));
        descriptionArea.setLineWrap(true);
        descriptionArea.setWrapStyleWord(true);
        JScrollPane scrollPane = new JScrollPane(descriptionArea);
        formPanel.add(scrollPane);
        
        // Total Amount
        formPanel.add(createLabel("Total Amount ($):"));
        totalAmountField = new JTextField();
        totalAmountField.setFont(new Font("Arial", Font.PLAIN, 12));
        formPanel.add(totalAmountField);
        
        // Advance Paid
        formPanel.add(createLabel("Advance Paid ($):"));
        advancePaidField = new JTextField();
        advancePaidField.setFont(new Font("Arial", Font.PLAIN, 12));
        formPanel.add(advancePaidField);
        
        mainPanel.add(formPanel, BorderLayout.CENTER);
        
        // Button panel
        JPanel buttonPanel = new JPanel();
        buttonPanel.setBackground(new Color(240, 240, 240));
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(10, 20, 20, 20));
        buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 10, 5));
        
        generateButton = new JButton("Generate Invoice");
        generateButton.setFont(new Font("Arial", Font.BOLD, 12));
        generateButton.setBackground(new Color(70, 130, 180));
        generateButton.setForeground(Color.WHITE);
        generateButton.setPreferredSize(new Dimension(150, 35));
        generateButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        generateButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                generateInvoice();
            }
        });
        buttonPanel.add(generateButton);
        
        viewInvoicesButton = new JButton("View Invoices");
        viewInvoicesButton.setFont(new Font("Arial", Font.BOLD, 12));
        viewInvoicesButton.setBackground(new Color(46, 125, 50));
        viewInvoicesButton.setForeground(Color.WHITE);
        viewInvoicesButton.setPreferredSize(new Dimension(150, 35));
        viewInvoicesButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        viewInvoicesButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                viewInvoices();
            }
        });
        buttonPanel.add(viewInvoicesButton);
        
        openPDFButton = new JButton("Open PDF");
        openPDFButton.setFont(new Font("Arial", Font.BOLD, 12));
        openPDFButton.setBackground(new Color(230, 126, 34));
        openPDFButton.setForeground(Color.WHITE);
        openPDFButton.setPreferredSize(new Dimension(150, 35));
        openPDFButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        openPDFButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                openPDF();
            }
        });
        buttonPanel.add(openPDFButton);
        
        mainPanel.add(buttonPanel, BorderLayout.SOUTH);
        
        add(mainPanel);
    }
    
    private JLabel createLabel(String text) {
        JLabel label = new JLabel(text);
        label.setFont(new Font("Arial", Font.BOLD, 12));
        label.setForeground(new Color(50, 50, 50));
        return label;
    }
    
    private void generateInvoice() {
        try {
            // Get input values
            String name = nameField.getText().trim();
            String phone = phoneField.getText().trim();
            String description = descriptionArea.getText().trim();
            String totalAmountStr = totalAmountField.getText().trim();
            String advancePaidStr = advancePaidField.getText().trim();
            
            // Validate inputs
            if (name.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter customer name.", 
                                            "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            
            if (phone.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter phone number.", 
                                            "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            
            if (description.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter description.", 
                                            "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            
            double totalAmount;
            double advancePaid;
            
            try {
                totalAmount = Double.parseDouble(totalAmountStr);
                advancePaid = Double.parseDouble(advancePaidStr);
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(this, "Please enter valid numbers for amounts.", 
                                            "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            
            // Create invoice
            Invoice invoice = service.createInvoice(name, phone, description, 
                                                     totalAmount, advancePaid);
            
            if (invoice == null) {
                JOptionPane.showMessageDialog(this, "Failed to create invoice. Please check your inputs.", 
                                            "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            
            // Generate PDF
            PDFGenerator.generatePDF(invoice);
            
            // Show success message
            JOptionPane.showMessageDialog(this, 
                "Invoice created successfully!\n\n" +
                "Invoice ID: INV-" + String.format("%03d", invoice.getInvoiceId()) + "\n" +
                "Customer: " + name + "\n" +
                "Amount: $" + String.format("%.2f", invoice.getTotalAmount()),
                "Success", JOptionPane.INFORMATION_MESSAGE);
            
            // Clear form
            clearForm();
            
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Error: " + e.getMessage(), 
                                        "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
    
    private void viewInvoices() {
        List<Invoice> invoices = InvoiceDatabase.loadAllInvoices();
        
        if (invoices.isEmpty()) {
            JOptionPane.showMessageDialog(this, "No invoices found in database.", 
                                        "View Invoices", JOptionPane.INFORMATION_MESSAGE);
            return;
        }
        
        // Create a dialog with list of invoices
        JDialog dialog = new JDialog(this, "View Invoices", true);
        dialog.setSize(600, 400);
        dialog.setLocationRelativeTo(this);
        
        JPanel dialogPanel = new JPanel(new BorderLayout(10, 10));
        dialogPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        // Create list model
        DefaultListModel<String> listModel = new DefaultListModel<>();
        for (Invoice inv : invoices) {
            String item = "INV-" + String.format("%03d", inv.getInvoiceId()) + " | " + 
                         inv.getCustomerName() + " | $" + 
                         String.format("%.2f", inv.getTotalAmount());
            listModel.addElement(item);
        }
        
        JList<String> invoiceList = new JList<>(listModel);
        invoiceList.setFont(new Font("Arial", Font.PLAIN, 12));
        JScrollPane scrollPane = new JScrollPane(invoiceList);
        dialogPanel.add(scrollPane, BorderLayout.CENTER);
        
        // Button panel
        JPanel btnPanel = new JPanel(new FlowLayout());
        
        JButton viewBtn = new JButton("View Details");
        viewBtn.addActionListener(e -> {
            int index = invoiceList.getSelectedIndex();
            if (index >= 0) {
                Invoice inv = invoices.get(index);
                JOptionPane.showMessageDialog(dialog, inv.toString(), 
                                            "Invoice Details", JOptionPane.INFORMATION_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(dialog, "Please select an invoice.", 
                                            "Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        btnPanel.add(viewBtn);
        
        JButton closeBtn = new JButton("Close");
        closeBtn.addActionListener(e -> dialog.dispose());
        btnPanel.add(closeBtn);
        
        dialogPanel.add(btnPanel, BorderLayout.SOUTH);
        
        dialog.add(dialogPanel);
        dialog.setVisible(true);
    }
    
    private void openPDF() {
        List<Invoice> invoices = InvoiceDatabase.loadAllInvoices();
        
        if (invoices.isEmpty()) {
            JOptionPane.showMessageDialog(this, "No invoices found.", 
                                        "Open PDF", JOptionPane.INFORMATION_MESSAGE);
            return;
        }
        
        // Create dialog to select invoice
        JDialog dialog = new JDialog(this, "Open Invoice PDF", true);
        dialog.setSize(500, 300);
        dialog.setLocationRelativeTo(this);
        
        JPanel dialogPanel = new JPanel(new BorderLayout(10, 10));
        dialogPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        // Create list model
        DefaultListModel<String> listModel = new DefaultListModel<>();
        for (Invoice inv : invoices) {
            String item = "INV-" + String.format("%03d", inv.getInvoiceId()) + " | " + 
                         inv.getCustomerName();
            listModel.addElement(item);
        }
        
        JList<String> invoiceList = new JList<>(listModel);
        invoiceList.setFont(new Font("Arial", Font.PLAIN, 12));
        JScrollPane scrollPane = new JScrollPane(invoiceList);
        dialogPanel.add(scrollPane, BorderLayout.CENTER);
        
        // Button panel
        JPanel btnPanel = new JPanel(new FlowLayout());
        
        JButton openBtn = new JButton("Open");
        openBtn.addActionListener(e -> {
            int index = invoiceList.getSelectedIndex();
            if (index >= 0) {
                Invoice inv = invoices.get(index);
                String fileName = "invoice_" + inv.getInvoiceId() + ".txt";
                PDFGenerator.openPDF(fileName);
                dialog.dispose();
            } else {
                JOptionPane.showMessageDialog(dialog, "Please select an invoice.", 
                                            "Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        btnPanel.add(openBtn);
        
        JButton cancelBtn = new JButton("Cancel");
        cancelBtn.addActionListener(e -> dialog.dispose());
        btnPanel.add(cancelBtn);
        
        dialogPanel.add(btnPanel, BorderLayout.SOUTH);
        
        dialog.add(dialogPanel);
        dialog.setVisible(true);
    }
    
    private void clearForm() {
        nameField.setText("");
        phoneField.setText("");
        descriptionArea.setText("");
        totalAmountField.setText("");
        advancePaidField.setText("");
        nameField.requestFocus();
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                InvoiceForm form = new InvoiceForm();
                form.setVisible(true);
            }
        });
    }
}

