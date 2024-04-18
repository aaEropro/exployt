from PyQt6.QtCore import *
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
from ui_selector import MainWindow
import os

SENTENCE_END = ['.']
EXCLAMATIONS = ['?','!']
PUNTUATUINS = [',', ';', ':', '…']
SPEECH = ['“', '”']
MISC = ['"', "'", "’", '*']

OVERRIDES = ['Mr', 'Ms', 'Mrs', 'Dr']
BYPASSES = ["I", "Ive", "Ill", "Id"]


DEBUG = True


class cleaner:
    to_replace = [
        ('—', ' -- '), ('-- ”', '--.”'),
        ('. . . .', '….'), ('. . .', '…'), ('....', '….'), ('...', '…'), ('. . .', '…'), (' …', '…'), 
        ('… ”', '….”'), ('…”', '….”'),
        ('?', '?.'), ('!', '!.'),

        # finishing
        ('..', '.'),
        ('  ', ' '), 
        ('*.', '.*'), ('*', '**')
    ]


    def _overrides(self, contents: str) -> str:

        titles = ['Mr', 'Ms', 'Mrs', 'Dr']
        special = ['The', 'And']

        for item in titles: contents = contents.replace(f'{item}.', f'{item.lower()}_')
        # for item in special: contents = contents.replace(item, item.lower())

        return contents


    def normalize_text(contents:str)->str:
        """
            replaces certain expressions
        """

        # for item in self.to_replace: contents = contents.replace(item[0], item[1])
        # contents = self._overrides(contents)

        return contents


    def strip_word(word: str) -> str:
        """
            removes all special characters from the given string.
        """
        markers = ['*', ',', '"', '“', '”', ".", "?", "!", "'", "’", '…', ':']

        for item in markers: word = word.replace(item, '')

        return word


    def clean_word(word:str) -> str:
        """
            removes all non sentence end characters from the given string.
        """
        markers = ['*', ',', '"', '“', '”', "'", "’"]

        for item in markers: word = word.replace(item, '')

        return word


class names:
    def _extend(self, name:str) -> str:
        if name[-1] != 's': return name+'s'
        else: return name


    def _normalize(self, contents:str, names:list) -> str:

        lines = contents.split('\n\n')
        new_text = list()
        newline = list()

        for line in lines:

            words = line.split()
            newline.clear()

            for word in words:

                cpy = word.replace('<ftime>', '').replace('</ftime>', '')
                cpy = cleaner.strip_word(cpy)

                if cpy not in (names + BYPASSES): newline.append(word.lower())
                else: newline.append(word)

            new_text.append(' '.join(newline))

        return '\n\n'.join(new_text)


    def _insert_tags(self, word:str) -> str:
        if word[0] in ['*', '"', '“', "'"]:
            word = f'{word[0]}<ftime>{word[1:]}'
        else: word = '<ftime>'+word

        if word[-1] in ['*', '"', '”', "'", ',', '?', '!', ':', ';', '…', '.']:
            word = f'{word[:-1]}</ftime>{word[-1]}'
        else: word += '</ftime>'

        return word


    def detect(self, contents: str):

        lines = contents.split('\n\n')

        names = set()
        new_lines = list()
        for line in lines:
            line = line.strip()
            words = line.split(" ")

            for index, word in enumerate(words):

                s_word = cleaner.strip_word(word)
                if len(s_word) == 0: continue

                start = False
                if index == 0: start = True
                else:
                    prev_word = cleaner.clean_word(words[index-1])
                    if len(prev_word) > 0 and prev_word[-1] in [".", '?', '!', '…', ':']:
                        start = True
                    elif word[0] in ['"', '“', ]: start = True

                if not start and s_word[0].isupper() and s_word not in names and s_word not in BYPASSES:
                    if DEBUG: words[index] = self._insert_tags(word)
                    names.add(s_word)
                    names.add(self._extend(s_word))

            new_lines.append(' '.join(words).replace('</ftime> <ftime>', ' '))

        return '\n\n'.join(new_lines), list(names)


def run(contents):

    contents = cleaner.normalize_text(contents)
    # print(contents)
    contents, names_list = names.detect(contents)

    if DEBUG:
        contents = names._normalize(contents, names_list)
        print(sorted(names_list), end='\n\n')

    return contents


if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = MainWindow()
    instance.show()
    app.exec()
    input_folder, output_folder = instance.data()

    # print(instance.data())

    input_folder, output_folder = ("/home/jovanni/Desktop/Fortune's Envoy-", "/home/jovanni/Desktop/Fortune's Envoy")
    
    if not os.path.isdir(input_folder): print('input directory error.'); sys.exit()
    
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    for path, directorys, files in os.walk(input_folder):
        for item in files:
            if item.endswith('.txt'):
                with open(os.path.join(input_folder, item), mode = 'r', encoding = "utf-8") as file:
                    contents = file.read()
                    file.close()

                newtext = run(contents)

                with open(os.path.join(output_folder, item), mode = 'w', encoding = "utf-8") as file:
                    file.write(newtext)
                    file.close()
        print(files)