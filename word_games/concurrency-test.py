import concurrent.futures
import time
from gtts import gTTS
import os
import glob

filepath = 'word_games/sounds/'

words = """
argument enjoyment merriment employment payment word work worm world worth
""".split()

def truncate_folder():
    input('press enter to truncate...')
    files = glob.glob(f'{filepath}*')
    for f in files:
        os.remove(f)
    input('press enter to continue...')

def generate_mp3s(word):
    myobj = gTTS(text=word, lang='en', slow=False)
    myobj.save(f"{filepath}{word}.mp3")
    myobj = gTTS(text=" ".join(word), lang='en', slow=True)
    myobj.save(f"{filepath}{word}_spell.mp3")

truncate_folder()

t1 = time.perf_counter()
for word in words:
    generate_mp3s(word)
print(f'baseline: {time.perf_counter() - t1}')

truncate_folder()

t1 = time.perf_counter()
with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(generate_mp3s, words)
print(f'ProcessPoolExecutor: {time.perf_counter() - t1}')

truncate_folder()

t1 = time.perf_counter()
with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(generate_mp3s, words)
print(f'ProcessPoolExecutor: {time.perf_counter() - t1}')

truncate_folder()
