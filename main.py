import func
import os

def run(contents):

    contents = func._clean(contents)
    contents = func._overrides(contents)

    names = func._detect_names(contents)

    contents = func._normalize(contents, names)

    return contents





PATH = '/home/jovanni/Desktop'
NAME = "Fortune's Envoy"

if __name__ == '__main__':
    for path, directorys, files in os.walk(os.path.join(PATH, NAME+'-')):
        for item in files:
            if item.endswith('.txt'):
                with open(os.path.join(os.path.join(PATH, NAME+'-'), item), mode = 'r', encoding = "utf-8") as file:
                    contents = file.read()
                    file.close()

                newtext = run(contents)

                with open(os.path.join(os.path.join(PATH, NAME), item), mode = 'w', encoding = "utf-8") as file:
                    file.write(newtext)
                    file.close()
        print(files)