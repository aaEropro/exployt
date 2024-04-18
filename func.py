import os

DEBUG = True

BYPASSES = ["I", "Ive", "Ill", "Id"]

def _clean(contents: str) -> str:

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


def _insert_tags(word:str) -> str:
    if word[0] in ['*', '"', '“', "'"]:
        word = f'{word[0]}<ftime>{word[1:]}'
    else: word = '<ftime>'+word

    if word[-1] in ['*', '"', '”', "'", ',', '?', '!', ':', ';', '…', '.']:
        word = f'{word[:-1]}</ftime>{word[-1]}'
    else: word += '</ftime>'

    return word



def _extend_names(names:list) -> list:
    ex_names = set()

    for name in names: 
        if name[-1] != 's': ex_names.add(name+'s')

    return names+list(ex_names)

def _extend(name:str) -> str:
    if name[-1] != 's': return name+'s'
    else: return name


def _ftime_detection(contents: str):

    lines = contents.split('\n\n')

    names = set()
    new_lines = list()
    for line in lines:
        line = line.strip()
        words = line.split(" ")

        for index, word in enumerate(words):

            s_word = _strip_word(word)
            if len(s_word) == 0: continue

            start = False
            if index == 0: start = True
            else:
                prev_word = _clean_word(words[index-1])
                if len(prev_word) > 0 and prev_word[-1] in [".", '?', '!', '…', ':']:
                    start = True
                elif word[0] in ['"', '“', ]: start = True

            if not start and s_word[0].isupper() and s_word not in names and s_word not in BYPASSES:
                if DEBUG: words[index] = _insert_tags(word)
                names.add(s_word)
                names.add(_extend(s_word))

        new_lines.append(' '.join(words).replace('</ftime> <ftime>', ' '))

    return '\n\n'.join(new_lines), list(names)

            


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

            cpy = cpy.replace('<ftime>', '').replace('</ftime>', '')
            
            cpy = _strip_word(cpy)

            # is not a name
            if cpy not in (names + BYPASSES): newline.append(word.lower())
            else: newline.append(word)

        new_text.append(' '.join(newline))

    return '\n\n'.join(new_text)
