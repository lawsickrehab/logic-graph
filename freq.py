#%%
from os import listdir
from articut import API
import json

#%%
# initilize variables
api = API()
folderPath = 'judgements/司法院－刑事補償_刑事'
textFiles = listdir(folderPath)
cache = {}

#%%
# Query API and store to cache
# TODO: Make it multi thread to speed up
countProgress = 0
for textFile in textFiles:
    countProgress += 1
    print(f'{folderPath}/{textFile}', f'{countProgress}/{len(textFiles)}')

    if textFile in cache:
        continue
    if textFile[-5:] != '.json':
        continue

    with open(f'{folderPath}/{textFile}') as file:
        judgements = json.loads(file.read())
        api.parse(judgements["judgement"])
        cache[textFile] = api.getNouns()

# %%
# Calc the frequency of nouns from cache
lawNounCount = {}
for fileName, sentences in cache.items():
    print(fileName)
    if sentences == None:
        continue
    with open(f'{folderPath}/{textFile}') as file:
        judgements = json.loads(file.read())
    relatedLaws = judgements['relatedIssues']
    relatedKeys = []

    for law in relatedLaws:
        key = f"{law['lawName']}-{law['issueRef']}"
        relatedKeys.append(key)
        if key not in lawNounCount:
            lawNounCount[key] = {}
    
    for sentence in sentences:
        for noun in sentence:
            for key in relatedKeys:
                if noun[-1] not in lawNounCount[key]:
                    lawNounCount[key][noun[-1]] = 1
                else:
                    lawNounCount[key][noun[-1]] += 1

# print(lawNounCount)
print(len(lawNounCount))
# %%
# Something can sort dictionary
for law, nouns in lawNounCount.items():
    test = sorted(nouns.items(), key=lambda item: item[1], reverse=True)
    print(law)
    print(test[0:10])
    






# %%
# Save cache to cache.json
def saveCache(cache) -> None:
    with open('cache.json', 'w') as file:
        json.dump(cache, file)
saveCache(cache)
# %%
# Load cache from cache.json
def loadCache() -> dict:
    with open('cache.json', 'r') as file:
        return json.loads(file.read())
cache = loadCache()
# %%
