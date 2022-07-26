#%%
from os import listdir
from articut import API
import json

#%%
api = API()
folderPath = 'judgements/司法院－刑事補償_刑事'
textFiles = listdir(folderPath)
cache = {}
#%%
countProgress = 0
for textFile in textFiles:
    countProgress += 1
    print(f'{folderPath}/{textFile}', f'{countProgress}/{len(textFiles)}')
    with open(f'{folderPath}/{textFile}') as file:
        judgements = json.loads(file.read())
        api.parse(judgements["judgement"])
        cache[textFile] = api.getNouns()

# %%
print(cache)
# %%
nounCount = {}
for fileName, sentences in cache.items():
    for sentence in sentences:
        for noun in sentence:
            if noun[-1] not in nounCount:
                nounCount[noun[-1]] = 1
            else:
                nounCount[noun[-1]] += 1

print(nounCount)
# %%
{k: v for k, v in sorted(nounCount.items(), key=lambda item: item[1])}
# %%
