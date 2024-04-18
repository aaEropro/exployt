import os
from ui_selector import *


SENTENCE_END = ['.']
EXCLAMATIONS = ['?','!']
PUNTUATUINS = [',', ';', ':', '…']
SPEECH = ['“', '”']
MISC = ['"', "'", "’", '*']

OVERRIDES = ['Mr', 'Ms', 'Mrs', 'Dr']
BYPASSES = ["I", "Ive", "Ill", "Id"]

class cleaner:
    to_replace = [
        ('—', ' -- '), ('-- ”', '--.”'),
        ('. . . .', '….'), ('. . .', '…'), ('....', '….'), ('...', '…'), ('. . .', '…'), (' …', '…'), 
        ('… ”', '….”'), ('…”', '….”'),
        ('?', '?.'), ('!', '!.'),
        ('.,', ','),

        # finishing
        ('..', '.'),
        ('  ', ' '), 
        ('*.', '.*'),
        ('“*', '*“'), ('*”', '”*')
        # ('*', '**')
    ]
    titles = ['Mr', 'Ms', 'Mrs', 'Dr']
    special = ['The', 'And']

    @staticmethod
    def _override(contents: str) -> str:
        for item in cleaner.titles: 
            contents = contents.replace(f'{item}.', f'{item.lower()}_')
        # for item in cleaner.special:
        #     contents = contents.replace(item, item.lower())

        return contents

    @staticmethod
    def sanitize(contents:str) -> str:
        for item in cleaner.to_replace: 
            contents = contents.replace(item[0], item[1])

        contents = cleaner._override(contents)

        return contents
    
    @staticmethod
    def strip(word: str) -> str:
        markers = ['*', '"', '“', '”', "'", "’", ".", ',', '…', ':', "?", "!"]

        for item in markers: word = word.replace(item, '')

        return word

    @staticmethod
    def clean(word:str) -> str:
        markers = ['*', ',', '"', '“', '”', "'", "’"]

        for item in markers: word = word.replace(item, '')

        return word
    


class name:
    @staticmethod
    def _extend(name:str) -> str:
        if name[-1] != 's': return name+'s'
        else: return name

    @staticmethod
    def _normalize(contents:str, names:list) -> str:

        lines = contents.split('\n\n')
        new_text = list()
        newline = list()

        for line in lines:

            words = line.split()
            newline.clear()

            for word in words:

                cpy = word.replace('<ftime>', '').replace('</ftime>', '')
                cpy = cleaner.strip(cpy)

                if cpy not in (names + BYPASSES): newline.append(word.lower())
                else: newline.append(word)

            new_text.append(' '.join(newline))

        return '\n\n'.join(new_text)

    @staticmethod
    def _insert_tags(word:str) -> str:
        if word[0] in ['*', '"', '“', "'"]:
            word = f'{word[0]}<ftime>{word[1:]}'
        else: word = '<ftime>'+word

        if word[-1] in ['*', '"', '”', "'", ',', '?', '!', ':', ';', '…', '.']:
            word = f'{word[:-1]}</ftime>{word[-1]}'
        else: word += '</ftime>'

        return word

    @staticmethod
    def detect(contents: str):

        lines = contents.split('\n\n')

        names = set()
        new_lines = list()
        for line in lines:
            line = line.strip()
            words = line.split(" ")

            for index, word in enumerate(words):

                s_word = cleaner.strip(word)
                if len(s_word) == 0: continue

                start = False
                if index == 0: start = True
                else:
                    prev_word = cleaner.clean(words[index-1])
                    if len(prev_word) > 0 and prev_word[-1] in [".", '?', '!', '…', ':']:
                        start = True
                    elif word[0] in ['"', '“', ]: start = True

                if not start and s_word[0].isupper() and s_word not in names and s_word not in BYPASSES:
                    words[index] = name._insert_tags(word)
                    names.add(s_word)
                    names.add(name._extend(s_word))

            new_lines.append(' '.join(words).replace('</ftime> <ftime>', ' '))

        return '\n\n'.join(new_lines), list(names)
    


def run(input_path:str, output_file:str, filename:str):
    with open(os.path.join(input_path, filename), 'r') as file:
        contents = file.read()

    contents = cleaner.sanitize(contents)
    contents, names = name.detect(contents)
    contents = name._normalize(contents, names)    

    with open(os.path.join(output_file, filename), 'w') as file:
        file.write(contents)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = MainWindow()
    instance.show()
    app.exec()

    input_folder, output_folder = instance.data()
    if not os.path.isdir(input_folder): print('input directory error.'); sys.exit()
    if not os.path.isdir(output_folder): os.mkdir(output_folder)

    for path, directorys, files in os.walk(input_folder):
        for item in files:
            if item.endswith('.txt'):
                run(path, output_folder, item)