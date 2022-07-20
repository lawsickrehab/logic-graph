from PyPDF2 import PdfReader
class pdfHandler:
    def pdf2txt(filename):
    reader = PdfReader("example.pdf")
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()