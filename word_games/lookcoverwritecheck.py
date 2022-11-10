import os
import playsound
import numpy as np
import pandas as pd
import time

class LookCoverWriteCheck():

    def __init__(self, words, sleeptime=0, practice=True):
        words if isinstance(words, list) else [words]
        self.words = {k.lower() : None for k in words}
        self.sounds_filepath = 'sound_assets/'
        self.sleeptime = sleeptime
        self.practice = practice

    def look(self, word):
        print(f'Look: {word}')
    
    def write(self, word):
        userinput = input('Write: ')
        self.words[word] = userinput.lower()
    
    def write_with_hints(self, word):
        i = 0
        while i < len(word):
            os.system('clear')
            print(' '.join(word[:i] + ('_' * (len(word) - i))))
            if input(f'\n\nWrite: ').lower() == word[i]:
                i += 1
        os.system('clear')
        print(' '.join(word))
    
    def check(self, word):
        return word == self.words[word]

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
            os.system('clear')
            self.look(word)
            self.pause()
            os.system('clear')
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
            self.pause()
            if self.practice and word != self.words[word]:
                self.write_with_hints(word)
        os.system('clear')
        self.results()

def main():
    words = """
    argument enjoyment merriment employment
    payment word work worm world worth
    """.split()
    LookCoverWriteCheck(words).run()

if __name__ == '__main__':
    main()
