from ArticutAPI import Articut
from pprint import pprint
import json

class API:
    def __init__(self) -> None:
        with open("account.json") as file:
            accountDict = json.loads(file.read())
        
        username = accountDict["email"]
        apikey = accountDict["apikey"]
        self.atc = Articut(username=username, apikey=apikey)

    def parse(self, str: str, level: str ='lv2'):
        self.result = self.atc.parse(str, level=level, chemicalBOOL=False)

    def getAllAttributes(self):
        attributes = []
        for sentence in self.result["result_obj"]:
            for word in sentence:
                if word["pos"] not in attributes:
                    attributes.append(word["pos"])
        attributes.sort()
        return attributes

    def getWordWithAttributes(self, attribute: str):
        ans = []
        for sentence in self.result["result_obj"]:
            for word in sentence:
                if word["pos"] == attribute and word["pos"] not in ans:
                    ans.append(word["text"])
        return ans
                

api = API()
with open("dist/101年度刑事具有參考價值之裁判要旨暨裁判全文-1.txt") as file:
    file.read(14688)
    testStr = file.read(768)
print(testStr)
api.parse(testStr, level='lv2')
print(api.atc.getPersonLIST(api.result))