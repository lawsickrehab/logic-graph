#%%
import os, time
from articut import API
import json
import threading
import queue
import re

#%%
# initilize
lock = threading.RLock()
threadNum = 6

print('Loading featured list...')
with open('Featured.txt') as file:
    data = file.readlines()
    featured = [i.strip() for i in data]

#%%
print('Loading all files...')
rootFolderPath = 'judgements'
allFiles = {}
for folder in os.listdir(rootFolderPath):
    if os.path.isdir(f'{rootFolderPath}/{folder}'):
        allFiles[folder] = []
        for file in os.listdir(f'{rootFolderPath}/{folder}'):
            if os.path.isfile(f'{rootFolderPath}/{folder}/{file}') and file[-5:] == '.json':
                allFiles[folder].append(file)

foundNum = 0
for folder, files in allFiles.items():
    foundNum += len(files)
print(f'{foundNum} files founded.')

# %%
# Save cache to cache.json
def saveCache(cache, subTitle) -> None:
    with open(f'cache/cache-{subTitle}.json', 'w') as file:
        json.dump(cache, file, ensure_ascii=False)

# %%
# Load cache from cache.json
def loadCache(subTitle):
    done = set()
    files = os.listdir('cache')
    for file in files:
        if os.path.isfile(f'cache/{file}') and len(re.findall(f'cache-{subTitle}-[0-9]+\.json', file)) == 1:
            with open(f'cache/{file}') as f:
                cachedNames = json.loads(f.read())
            for cachedName in cachedNames:
                done.add(cachedName)
            if len(cachedNames) < 1000:
                cache = cachedNames.copy()
    return cache, done


#%%
# Function to query API
def queryAPI(threadNum):
    api = API()
    while textFiles.qsize() > 0:
        textFile = textFiles.get()
        with lock:
            if textFile in done:
                textFiles.task_done()
                continue
        with open(textFile) as file:
            judgements = json.loads(file.read())
        while True:
            api.parse(judgements["judgement"])
            try:
                dict(api.result)
            except:
                continue
            break
        with lock:
            cache[textFile] = api.result
            done.append(textFile)
        textFiles.task_done()
    print(f'Thread {threadNum} stopped.')

# Function to show process and calcuate reamining time
def progress(event: threading.Event):
    startTime = time.time()
    allFilesNum = textFiles.qsize()
    while not event.is_set():
        remainingFilesNum = textFiles.qsize()
        usedTime = time.time() - startTime
        processedFilesNum = allFilesNum - remainingFilesNum
        ETR = (usedTime / processedFilesNum) * remainingFilesNum / 60 if processedFilesNum > 0 else 'inf' 
        print(f'{processedFilesNum}/{allFilesNum}, ETR: {ETR} mins.')
        time.sleep(5)
    print('Progress stopped.')

def autoSave(cache: dict, folder, event: threading.Event):
    counter = 0
    while not event.is_set():
        if counter > 180:
            with lock:
                cacheCP = cache.copy()
            saveCache(cacheCP, folder)
            print('Auto saved.')
            counter = 0
        time.sleep(1)
        counter += 1
    print('AutoSave stopped.')

#%%
# Query API and store to cache
for folder, files in allFiles.items():
    print(f'Loading files under {folder} into queue')
    textFiles = queue.Queue()
    for file in files:
        textFiles.put(f'{rootFolderPath}/{folder}/{file}')

    print(f'Loading cache for {folder}')
    cache, done = loadCache(folder)

    event = threading.Event()

    print(f'Start querying with {threadNum} threads.')
    tProgress = threading.Thread(target=progress, args=(event,), daemon=True)
    tAutoSave = threading.Thread(target=autoSave, args=(cache, folder, event,), daemon=True)
    tProgress.start()
    tAutoSave.start()
    for i in range(threadNum):
        threading.Thread(target=queryAPI, args=(i,), daemon=True).start()

    textFiles.join()

    event.set()
    tProgress.join()
    tAutoSave.join()

    with lock:
        saveCache(cache, folder)
    
    print(f'Files under folder {folder} successfully saved to cache file.')


# %%
# Calc the frequency of nouns from cache
lawNounCount = {}
for fileName, sentences in cache.items():
    print(fileName)
    if sentences == None:
        continue
    with open(fileName) as file:
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
freqNouns = {}
for law, nouns in lawNounCount.items():
    test = sorted(nouns.items(), key=lambda item: item[1], reverse=True)
    freqNouns[law] = test[0:50]

with open('freq.json', 'w') as file:
    json.dump(freqNouns, file)
    

print('Output Saved')




# %%
