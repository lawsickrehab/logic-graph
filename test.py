from PyPDF2 import PdfReader
from isort import file
class pdfHandler:
    def pdf2txt(filename):
        reader = PdfReader("src/" + filename)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        text = page.extract_text()
        return text