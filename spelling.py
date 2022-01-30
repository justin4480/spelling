from gtts import gTTS
import os
import numpy as np
import playsound
import pandas as pd
import time

PATH = os.getcwd() + '/spelling/sounds/'
# words = 'happily softly nervously tidily kindly nastily carefully quietly noisily'.split()
words = 'nastily carefully quietly'.split()
scores = np.empty(len(words), dtype='int32')
slow = False
times = [-1]
attempts = 0

def sayit(text, lang='en', slow=False):
    if False:
        # print(text)
        pass
    else:
        myobj = gTTS(text=text, lang=lang, slow=slow)
        myobj.save(PATH + "tts.mp3")
        playsound.playsound(PATH+"tts.mp3", True)
        os.remove(PATH + "tts.mp3")

while scores.sum(axis=0).max() < len(words):
    start_time = time.time()
    attempts += 1
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"-"*30}\nattempt number {attempts}\n{"-"*30}')
    sayit(f'attempt number {attempts}')
    score_round = []
    for word in words:
        sayit(word)
        answer = input('enter: ')
        if answer.lower() == word.lower():
            score_round.append(1)
            sayit('correct, well done Chloe')
        else:
            score_round.append(0)
            print(word)
            sayit(f'incorrect, {" ".join(word)}')
    
    times.append(int(time.time() - start_time))
    scores = np.column_stack((scores, score_round))
    correct = scores[:, -1].sum()
    sayit(f'{correct} out of {len(words)}')

    if correct == len(words):
        a = pd.DataFrame(
            data=scores,
            index=words,
            columns=[f'round {i}' for i in range(scores.shape[1])]
        ).T
        a['total'] = a.sum(axis=1)
        a['duration'] = times
        print(a.iloc[1:].T)
        sayit('Congratulations Chloe.  Full marks!')
    else:
        sayit('Lets try again Chloe.')

#            round 1  round 2  round 3  round 4
# nastily          0        0        0        1
# carefully        0        1        1        1
# quietly          0        1        1        1
# total            0        2        2        3
# duration       448      245      200       96