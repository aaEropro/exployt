import os

BYPASSES = ["I", "I've", "I'll", "I'd"]

def _clean(contents: str) -> str:

    to_replace = [
        ('—', ' -- '), ('-- ”', '--.”'),
        ('. . . .', '….'), ('. . .', '…'), ('....', '….'), ('...', '…'), ('. . .', '…'), (' …', '…'), 
        ('?', '?.'), ('!', '!.'),

        # finishing
        ('..', '.'),
        ('  ', ' '), 
        ('*.', '.*'), ('*', '**')
    ]
    for item in to_replace: contents = contents.replace(item[0], item[1])

    return contents


def _overrides(contents: str) -> str:

    titles = ['Mr', 'Ms', 'Mrs', 'Dr']
    special = ['The', 'And']

    for item in titles: contents = contents.replace(f'{item}.', f'{item.lower()}_')
    for item in special: contents = contents.replace(item, item.lower())

    return contents


def _strip_word(word: str) -> str:
    markers = ['*', ',', '"', '“', '”', ".", "?", "!", "'", "’", '…', ':']

    for item in markers: word = word.replace(item, '')

    return word


def _clean_word(word:str) -> str:
    markers = ['*', ',', '"', '“', '”', "'", "’"]

    for item in markers: word = word.replace(item, '')

    return word


def _detect_names(contents: str) -> list:

    lines = contents.split('\n\n')

    names = list()
    for line in lines:
        words = line.split(" ")

        for index, word in enumerate(words):
            
            word = _strip_word(word)

            start = False
            if index == 0:
                start = True

            # check for sentence start
            else:
                prev = words[index-1]
                prev = _clean_word(prev)

                # chech if previous is sentence end
                if len(prev) > 0 and prev[-1] in [".", '?', '!', '…', ':']:
                    start = True

            # pass over 0-length words
            if len(word) == 0:
                pass

            # chech if the word is a new name and append it
            elif (not start) and word[0].isupper() and (word not in names) and (word not in BYPASSES):
                names.append(word)

    return names


def _normalize(contents:str, names:list) -> str:

    lines = contents.split('\n\n')
    new_text = list()
    newline = list()

    for line in lines:

        words = line.split()
        newline.clear()

        for word in words:

            cpy = word
            
            cpy = _strip_word(cpy)

            # is not a name
            if cpy not in (names + BYPASSES): newline.append(word.lower())
            else: newline.append(word)

        new_text.append(' '.join(newline))

    return '\n\n'.join(new_text)


def run(contents):

    contents = _clean(contents)
    contents = _overrides(contents)

    names = _detect_names(contents)

    contents = _normalize(contents, names)

    return contents
    




if __name__ == '__main__':
    for path, directorys, files in os.walk(r"C:\Users\jovanni\Desktop\Dune-"):
        for item in files:
            if item.endswith('.txt'):
                with open(os.path.join(r"C:\Users\jovanni\Desktop\Dune-", item), mode = 'r', encoding = "utf-8") as file:
                    contents = file.read()
                    file.close()

                newtext = run(contents)

                with open(os.path.join(r"C:\Users\jovanni\Desktop\Dune", item), mode = 'w', encoding = "utf-8") as file:
                    file.write(newtext)
                    file.close()
        print(files)