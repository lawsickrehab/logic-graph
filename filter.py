import re

class filter:

    regxs = [
        '[，。；]按.+?。',
        '[，。；]而.+?。',
        '固然.+?，然[^。]+?。', # 不會選最近的句號
        '具體言之.+?[，。]可以.+?加以綜合判斷',
        '尚應權衡.+?為一整體性判斷',
        '倘.+?則.+?但.+?。',
        '按.+?[，。]除.+?。',
        '故倘.+?縱令.+?於新法生效施行後，即.+?。',
        '原則上.+?例外.+?。'
    ]
    
    def selectRegx(self):
        for idx, regx in enumerate(self.regxs):
            print(f'{idx}: {regx}')

    def find(self, regx, text: str):
        return re.findall(regx, text)

