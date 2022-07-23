from os import listdir
class pdfHandler:
    def halfWidth2FullWidth(str):
        str = str.replace('\n', '')
        str = str.replace('(', '（')
        str = str.replace(')', '）')
        str = str.replace('.', '。')
        str = str.replace(',', '，')
        str = str.replace('?', '？')
        str = str.replace(';', '；')
        str = str.replace(':', '：')
        return str
    def halfWidth2FullWidthFile(filename):
        ifs = open("dist/" + filename, "r", encoding="UTF-8")
        content = ifs.read()
        content = pdfHandler.halfWidth2FullWidth(content)
        ifs.close()
        ofs = open("dist/" + filename, "w+", encoding="UTF-8")
        ofs.write(content)
        ofs.close()
    def halfWidth2FullWidthAll():
        filenames = listdir("dist")
        for i in range(len(filenames)):
            filename = filenames[i]
            print(f"processing file [{i + 1}/{len(filenames)}]:", filename)
            pdfHandler.halfWidth2FullWidthFile(filename)
pdfHandler.halfWidth2FullWidthAll()