@echo off
cd /d "%~dp0"
java -cp "iText7-Core-7.2.0\kernel-7.2.0.jar;iText7-Core-7.2.0\io-7.2.0.jar;iText7-Core-7.2.0\layout-7.2.0.jar;iText7-Core-7.2.0\commons-7.2.0.jar;." InvoiceForm
pause
