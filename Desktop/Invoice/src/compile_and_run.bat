@echo off
cd /d "%~dp0"
echo Compiling Invoice Generator...
javac -cp "iText7-Core-7.2.0\kernel-7.2.0.jar;iText7-Core-7.2.0\io-7.2.0.jar;iText7-Core-7.2.0\layout-7.2.0.jar;iText7-Core-7.2.0\commons-7.2.0.jar" -source 8 -target 8 Invoice.java InvoiceService.java PDFGenerator.java InvoiceDatabase.java InvoiceForm.java
if errorlevel 1 (
    echo Compilation failed!
    pause
    exit /b 1
)
echo Compilation successful!
echo.
echo Starting Invoice Generator...
java -cp "iText7-Core-7.2.0\kernel-7.2.0.jar;iText7-Core-7.2.0\io-7.2.0.jar;iText7-Core-7.2.0\layout-7.2.0.jar;iText7-Core-7.2.0\commons-7.2.0.jar;." InvoiceForm
pause
