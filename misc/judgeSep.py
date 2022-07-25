from os import listdir, mkdir
SRCPATH = "txtFormatted"
DISTDIR = "judges/_auto"
errors = []
class judgeSep:
    def getPosContent(text):
        pos0 = text[:30000].rfind("。。。。。。。。。")
        middle = text[pos0:pos0 + 50]
        posContent = pos0 + middle.find("一、")
        if(posContent == -1):
            posContent = middle.find("最高法院")
        return posContent
    def getContentOfTextItemList(titleAndContentOfText):
        contentOfText = titleAndContentOfText[titleAndContentOfText.find("一、"):]
        contentOfTextItemList = []
        ENGNUMLIST = [str(i) for i in range(10)]
        while True:
            curBeginPos = 0
            curEndPos = contentOfText.find("。。。")
            if(curEndPos == -1):
                break
            contentOfTextItem = contentOfText[curBeginPos: curEndPos]
            contentOfTextItemList.append(contentOfTextItem)
            nxtBeginPos = curEndPos + 1
            while True:
                if nxtBeginPos < 0 or nxtBeginPos >= len(contentOfText):
                    break
                curChar = contentOfText[nxtBeginPos]
                if curChar != ' ' and curChar != '。' and curChar not in ENGNUMLIST:
                    if curChar == '裁':
                        if nxtBeginPos <= len(contentOfText) - 4:
                            if contentOfText[nxtBeginPos:nxtBeginPos + 4] == "裁判全文":
                                nxtBeginPos += 4
                    if curChar == '年':
                        nxtBeginPos -= 3
                    break
                nxtBeginPos += 1
                continue
            contentOfText = contentOfText[nxtBeginPos:]
        # [print(x) for x in contentOfTextItemList]
        return contentOfTextItemList
    def sepContentOfTextAndContent(text):
        posContent = judgeSep.getPosContent(text)
        titleAndContentOfText = text[:posContent]
        content = text[posContent:]
        contentOfTextItemList = judgeSep.getContentOfTextItemList(titleAndContentOfText)
        return (contentOfTextItemList, content)
    def getContentItemList(filename, contentOfTextItemList, content):
        contentItemList = []
        for i in range(len(contentOfTextItemList)):
            print(f"i = {i} / {len(contentOfTextItemList) - 1}")
            # print(f"\tcontentOfTextItemList[{i}] = {contentOfTextItemList[i]}")
            if(i == len(contentOfTextItemList) - 1):
                # print("case 1")
                endPos = len(content)
            elif contentOfTextItemList[i + 1][0:5].find('、') != -1:
                # print("case 2")
                if contentOfTextItemList[i + 1] == "四、108年度台上字第441號":
                    contentOfTextItemList[i + 1] = "四、108年度台上字第411號"
                    print("四、108年度台上字第411號")
                    exit(1)
                endPos = content.find(contentOfTextItemList[i + 1])
            elif filename in ["103年度刑事具有參考價值之裁判要旨暨裁判全文.txt", "104年度刑事具有參考價值之裁判要旨暨裁判全文.txt"] and content[10:].find("【裁判字號】") != -1:
                endPos = content[10:].find("【裁判字號】") + 10
            elif content[10:].find("裁判字號：") != -1:
                # print("case 3")
                endPos = content[10:].find("裁判字號：") + 10
                if(content[30:endPos].find("機密案件，不予公開。") != -1):
                    endPos = content[:endPos].rfind("年度台上字第") - 3
                if(content[30:endPos].find("依法屬不得公開之案件") != -1 or content[30:endPos].find("依法屬不得公開案件") != -1):
                    # print("依法屬不得公開案件 / 依法屬不得公開之案件")
                    if(contentOfTextItemList[i + 1] == "108年度台抗字第1489號"):
                        endPos = content[:endPos].rfind("年度台抗字第") - 3
                    else:
                        endPos = content[:endPos].rfind("年度台上字第") - 3
            else: 
                # print("case 4")
                endPos = content[10:].find("最高法院") + 10
                if(endPos == -1):
                    print(f"content ({len(content)})= {content}")
                    exit(1)
                while content[endPos:endPos + 10].find("裁判書") == -1:
                    if(content[endPos + 1:].find("最高法院") == -1):
                        endPos = len(content)
                        break
                    endPos = content[endPos + 1:].find("最高法院") + endPos + 1
                if(content[30:endPos].find("機密案件，不予公開。") != -1):
                    endPos = content[:endPos].rfind("年度台上字第") - 3
                if(content[30:endPos].find("依法屬不得公開之案件") != -1 or content[30:endPos].find("依法屬不得公開案件") != -1):
                    # print("依法屬不得公開案件 / 依法屬不得公開之案件")
                    endPos = content[:endPos].rfind("年度台上字第") - 3
            # print(f"content[:endPos] = ({len(content[:endPos])})\t\t{content[:endPos][:30]}...{content[:endPos][50:100]}...{content[:endPos][-30:]}")
            # print(f"endPos = {endPos}")
            if(endPos == 0 or endPos == -1):
                errors.append((filename, i))
                print(f"endPos = {endPos}")
                exit(-1)
            contentItemList.append(content[:endPos])
            content = content[endPos:]
            # print(f"len(content) = {len(content)}")
        return contentItemList
    def judgeSep(filename):
        ifs = open(SRCPATH + "/" + filename, "r", encoding="UTF-8")
        text = ifs.read()
        ifs.close()
        (contentOfTextItemList, content) = judgeSep.sepContentOfTextAndContent(text)
        contentItemList = judgeSep.getContentItemList(filename, contentOfTextItemList, content)
        # DISTPATH = DISTDIR + "/" + filename.replace('.txt','')
        # mkdir(DISTPATH)
        # for i in range(len(contentOfTextItemList)):
        #     print(f"\t\twriting to file [{i + 1}/{len(contentOfTextItemList)}]:{DISTPATH}/{contentOfTextItemList[i]}")
        #     f = open(DISTPATH + "/" + contentOfTextItemList[i] + ".txt", "w+", encoding="UTF-8")
        #     f.write(contentItemList[i])
        #     f.close()
    def judgeSepAll():
        filenames = listdir(SRCPATH)
        for i in range(len(filenames)):
            filename = filenames[i]
        for filename in ["109年度（9月）刑事具有參考價值之裁判要旨暨裁判全文.txt"]:
            print(f"processing file [{i + 1}/{len(filenames)}]:", filename)
            judgeSep.judgeSep(filename)
judgeSep.judgeSepAll()