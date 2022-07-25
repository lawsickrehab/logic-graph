#%%
from os import listdir
from articut import API

#%%
api = API()
folderPath = 'judges/_auto/最高法院刑事具有參考價值之裁判要旨暨裁判全文（109年度11月）'
textFiles = listdir(folderPath)
cache = {}
#%%
for textFile in textFiles:
    with open(f'{folderPath}/{textFile}') as file:
        judgements = file.read()
        api.parse(judgements)
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
