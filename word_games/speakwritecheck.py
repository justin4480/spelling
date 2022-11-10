import os
import concurrent.futures
import numpy as np
import pandas as pd
import time
import glob
from gtts import gTTS
import playsound

class SpeakWriteCheck:

    def __init__(self, words, practice=True, sleeptime=0):
        words if isinstance(words, list) else [words]
        self.words = {k.lower() : '' for k in words}
        self.sounds_filepath = 'sound_assets/'
        self.words_filepath = 'pre_cache_sounds/'
        self.sleeptime = sleeptime
        self.practice = practice
        self.truncate_folder()
        self.generate_mp3s()

    def truncate_folder(self):
        files = glob.glob(f'{self.words_filepath}*')
        for f in files:
            os.remove(f)

    def generate_mp3s(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.generate_mp3, self.words)

    def generate_mp3(self, word):
        # word mp3
        myobj = gTTS(text=word, lang='en', slow=False)
        myobj.save(f"{self.words_filepath}{word}.mp3")
        # spelling mp3
        myobj = gTTS(text=" ".join(word), lang='en', slow=True)
        myobj.save(f"{self.words_filepath}{word}_spell.mp3")

    def trash_mp3s(self):
        pass
    
    def write(self, word):
        userinput = input('Write: ')
        self.words[word] = userinput.lower()

    def check(self, word):
        return word == self.words[word]
    
    def write_with_hints(self, word):
        i = 0
        while i < len(word):
            os.system('clear')
            print(' '.join(word[:i] + ('_' * (len(word) - i))))
            if input(f'\n\nWrite: ').lower() == word[i]:
                i += 1
        os.system('clear')
        print(' '.join(word))

    def results(self):
        results = pd.DataFrame(self.words.items(), columns=['answer', 'guess'])
        results['results'] = np.where(
            results.answer == results.guess, 'Correct', 'Incorrect')
        print(results)

    def pause(self):
        if self.sleeptime == 0:
            input('\n\npress enter when ready.. ')
        else:
            time.sleep(self.sleeptime)
    
    def run(self):
        for word in self.words.keys():
            while len(self.words[word]) == 0:
                os.system('clear')
                playsound.playsound(f'{self.words_filepath}{word}.mp3')
                self.write(word)
            if self.check(word):
                os.system('clear')
                print('Correct')
                playsound.playsound(f'{self.sounds_filepath}correct.mp3')
            else:
                os.system('clear')
                print(f'Guess:  {self.words[word]}')
                print(f'Answer: {word}')
                playsound.playsound(f'{self.sounds_filepath}wrong.wav')
                playsound.playsound(f'{self.words_filepath}{word}.mp3')
                playsound.playsound(f'{self.words_filepath}{word}_spell.mp3')
                if self.practice:
                    self.write_with_hints(word)
            self.pause()
        os.system('clear')
        self.truncate_folder()
        self.results()
        self.pause()

    
def main():
    words = """
    argument enjoyment merriment employment
    payment word work worm world worth
    """.split()
    SpeakWriteCheck(words).run()

if __name__ == '__main__':
    main()
