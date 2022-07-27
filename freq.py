#%%
import os, time
from articut import API
import json
import threading
import queue

#%%
# initilize
lock = threading.RLock()
threadNum = 12

print('Loading all files...')
rootFolderPath = 'judgements'
textFiles = queue.Queue()
for path, subdirs, files in os.walk(rootFolderPath):
    for name in files:
        if name[-5:] == '.json':
            textFiles.put(os.path.join(path, name))
print(f'{textFiles.qsize()} files loaded.')

#%%
cache = {}

#%%
# Function to query API
def queryAPI():
    api = API()
    while True:
        textFile = textFiles.get()
        with lock:
            if textFile in cache:
                textFiles.task_done()
                continue
        with open(textFile) as file:
            judgements = json.loads(file.read())
        api.parse(judgements["judgement"])
        with lock:
            cache[textFile] = api.getNouns()
        textFiles.task_done()

# Function to show process and calcuate reamining time
def progress():
    startTime = time.time()
    allFilesNum = textFiles.qsize()
    while textFiles.qsize() > 0:
        remainingFilesNum = textFiles.qsize()
        usedTime = time.time() - startTime
        processedFilesNum = allFilesNum - remainingFilesNum
        ETR = (usedTime / processedFilesNum) * remainingFilesNum / 60 if processedFilesNum > 0 else 'inf' 
        print(f'{processedFilesNum}/{allFilesNum}, ETR: {ETR} mins.')
        time.sleep(5)

#%%
# Query API and store to cache
print(f'Start querying with {threadNum} threads.')

threading.Thread(target=progress, daemon=True).start()
for i in range(threadNum):
    threading.Thread(target=queryAPI, daemon=True).start()

textFiles.join()


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
# print(len(lawNounCount))
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
