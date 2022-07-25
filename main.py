#%%
from filter import filter

data = ''

with open('tmp.txt', 'r') as file:
    data = file.read()
    data = data.replace('\n', '')

with open('tmp.txt', 'w') as file:
    file.write(data)
    
# %%
for regx in filter().regxs:
    print(regx)
    print(filter().find(regx, data))
# %%
