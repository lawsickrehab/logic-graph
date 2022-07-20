import re

class filter:

    regxs = [
        '[，。；]按.+?。',
        '[，。；]而.+?。',
        '固然.+?，然[^。]+?。', # 不會選最近的句號
        '具體言之.+?[，。]可以.+?加以綜合判斷',
        '尚應權衡.+?為一整體性判斷',
        '倘.+?則.+?但.+?。',
        '按.+?[，。]除.+?。'
    ]
    
    def find(self, regx, text: str):
        return re.findall(regx, text)


# hell