#%%
from ArticutAPI import Articut
import json
import re

#%%
class API:
    def __init__(self) -> None:
        with open("account.json") as file:
            accountDict = json.loads(file.read())
        
        username = accountDict["email"]
        apikey = accountDict["apikey"]
        self.atc = Articut(username=username, apikey=apikey)

        self.regxs1 = map(re.compile, [
            '<RANGE_locality>上</RANGE_locality><ACTION_verb>開</ACTION_verb><FUNC_inner>所</FUNC_inner><ACTION_verb>謂</ACTION_verb>.*?<FUNC_inter>即</FUNC_inter><MODAL>該</MODAL><ACTION_verb>當</ACTION_verb><FUNC_inner>之</FUNC_inner>',
            '<ACTION_verb>按</ACTION_verb>.*?，<FUNC_inter>而</FUNC_inter>.*?。',
            '<MODIFIER>固然</MODIFIER>.*?<FUNC_inter>然</FUNC_inter>.*?<FUNC_inner>自</FUNC_inner>.*?。'
        ])

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

    def getResultWithTags(self, join: bool =False):
        if join:
            return ''.join(self.result["result_pos"])
        else:
            return self.result["result_pos"]

    def removeTags(self, preString: str):
        regx = "<[^<]*?>"
        return re.sub(regx, '', preString)

    def getLawReason(self):
        for regx in self.regxs1:
            for match in regx.findall(self.getResultWithTags(join=True)):
                print(self.removeTags(match))
            
    
                
#%%
api = API()
with open("test.txt") as file:
    testStr = file.read()
api.parse(testStr)

#%%
api.getLawReason()

# %%
api.getResultWithTags(True)
# %%
