import re

class filter:
    regxs = [
        '[，,。]按*。',
        '[，,。]而*。',
        '固然*；然*自*。',
        '具體言之*可以*加以綜合判斷*。'
    ]

    def find(self, text: str, regx):
        return re.search(regx, text)
