import os
import json


def make_directory(words, parent='./fake'):

    if not words:
        return
    word = words.pop(0)
    word_path= os.path.join(parent,word)
    dir_name = word_path
    print(dir_name)
    os.makedirs(dir_name, exist_ok=True)
    file1_word = word_path
    write_words(word_path,words,dir_name)


    add_more_files(words,dir_name, 3)
    make_directory(words,dir_name)


def add_more_files(words, path_prefix, count=1 ):
    for counter in range(count):
        if words:
            word_path= os.path.join(path_prefix,words.pop(0))
            write_words(word_path, words, path_prefix)

def write_words(file, words, dir_name):
    print(f"{file} {dir_name}")
    for extension in ['.py','.txt','.help','.md', '.meta']:
        with open(os.path.join(f"{file}{extension}"), "w") as f:
            f.write(json.dumps(words))

if __name__ == '__main__':
    # Example usage:
    words_list = ['quack', 'apple', 'castle', 'labyrinth', 'yoga', 'zephyr', 'harmonica', 'sunrise', 'xylophone', 'violin', 'whale', 'bomb', 'zebra', 'tiger', 'jelly', 'galaxy', 'chestnut', 'kangaroo', 'penguin', 'cactus', 'daisy', 'mushroom', 'umbrella', 'cherry', 'volcano', 'octopus', 'pineapple', 'squirrel', 'giraffe', 'whisper', 'moonlight', 'piano', 'wolf', 'lighthouse', 'feather', 'ocean', 'butterfly', 'tulip', 'mammoth', 'rabbit', 'raccoon', 'igloo', 'nightingale', 'yacht', 'echo']
    make_directory(words_list)
