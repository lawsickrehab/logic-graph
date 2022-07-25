from PyPDF2 import PdfReader
from os import listdir

SRCPATH = "pdf"
DISTPATH = "txt"

missingPageslist = []
class pdfHandler:
    def pdf2txt(filename):
        missingPages = []
        reader = PdfReader("src/" + filename)
        number_of_pages = len(reader.pages)
        numPages = reader.numPages
        texts = ""
        for _ in range(numPages):
            if (_ % 50 == 0):
                print(f"\tprocessing page [{_}/{numPages}]")
            page = reader.pages[_]
            try:
                text = page.extract_text()
                texts = texts + text
            except:
                missingPages.append(_)
        missingPageslist.append((filename, missingPages))
        return texts
    
    def exec():
        filenames = listdir(SRCPATH)
        for i in range(len(filenames)):
            filename = filenames[i]
            print(f"processing file [{i + 1}/{len(filenames)}]:", filename)
            context = pdfHandler.pdf2txt(filename)
            f = open(DISTPATH + "/" + filename.replace(".pdf", ".txt"), "w+", encoding="UTF-8")
            f.write(context)
            f.close()
        print("Finished!")
        print("Missing Pages")
        for x in missingPageslist:
            print(f"{x[0]}\t{x[1]}")
