from datetime import datetime
from turtle import st
from gtts import gTTS
import pandas as pd
import playsound
import os
import sqlite3

con = sqlite3.connect('my-test.db')
cur = con.cursor()

def sayit(text: str, lang: str='en', slow: bool=False, audio: bool=True):
    if audio:
        myobj = gTTS(text=text, lang=lang, slow=slow)
        myobj.save("tts.mp3")
        playsound.playsound("tts.mp3", True)
        os.remove("tts.mp3")
    else:
        print(text)


class User:

    def __init__(self, username: str):
        self.db_table = 'user'
        self.uid = None
        self.username = username
        self.name = None
        self.login() if self.db_check_exists() else self.register()

    def login(self):
        while True:
            password = input('Password: ')
            cur.execute(f"SELECT password FROM {self.db_table} WHERE username = '{self.username}'")
            if password != cur.fetchone()[0]:
                print('Incorrect, try again')
            else:
                break
        self.db_get()

    def register(self):
        print('Please register')
        self.name = input('Name: ')
        password = input('Password: ')
        self.db_insert(password)
    
    def change_password(self):
        while True:
            password = input('Old password: ')
            cur.execute(f"SELECT password FROM {self.db_table} WHERE username = '{self.username}'")
            if password != cur.fetchone()[0]:
                print('Incorrect, try again')
            else:
                new_password = input('New password: ')
                cur.execute(f"UPDATE {self.db_table}  set password = '{new_password}' where username = '{self.username}'")
                con.commit()
                break                
    
    def get_report():
        pass
    
    def db_check_exists(self) -> bool:
        cur.execute(f"SELECT EXISTS (SELECT * FROM {self.db_table} WHERE username = '{self.username}')")
        return cur.fetchone()[0] == 1

    def db_insert(self, password: str):
        cur.execute(
            f"INSERT INTO {self.db_table} (username, name, password)\n"
            f"VALUES('{self.username}', '{self.name}', '{password}');"
        )
        con.commit()
    
    def db_get(self):
        cur.execute(f"SELECT uid, username, name FROM {self.db_table} WHERE username = '{self.username}'")
        self.uid, self.username, self.name, = cur.fetchone()
        # print(f'Welcome back {self}')

    def __repr__(self) -> str:
        return f'{self.name}'


class Wordgroup:
    def __init__(self, name: str):
        self.db_table = 'wordgroup'
        self.gid = None
        self.name = name
        self.db_get() if self.db_check_exists() else self.db_insert()
    
    def add_words(self, words: list):
        self.words = [Word(word, self.gid) for word in words]
    
    def get_words(self):
        cur.execute(
            f"select w.name\n"
            f"from {self.db_table} as wg\n"
            f"inner join word as w on w.gid = wg.gid\n"
            f"where wg.name = '{self.name}'"
        )
        words = cur.fetchall()
        return [Word(word[0]) for word in words]
    
    def db_check_exists(self) -> bool:
        cur.execute(f"SELECT EXISTS (SELECT * FROM {self.db_table} WHERE name = '{self.name}')")
        return cur.fetchone()[0] == 1
    
    def db_insert(self):
        cur.execute(f"INSERT INTO {self.db_table} (name) VALUES('{self.name}');")
        con.commit()
        self.db_get()
    
    def db_get(self):
        cur.execute(f"SELECT gid, name FROM {self.db_table} WHERE name = '{self.name}'")
        self.gid, self.name = cur.fetchone()

    def __repr__(self) -> str:
        return f'{self.name} {self.words}'


class Word:
    def __init__(self, name: str, gid: int=None):
        self.db_table = 'word'
        self.wid = None
        self.gid = gid
        self.name = name
        self.db_get() if self.db_check_exists() else self.db_insert()
    
    def db_check_exists(self) -> bool:
        cur.execute(f"SELECT EXISTS (SELECT * FROM {self.db_table} WHERE name = '{self.name}')")
        return cur.fetchone()[0] == 1
    
    def db_insert(self):
        cur.execute(f"INSERT INTO {self.db_table} (gid, name) VALUES('{self.gid}', '{self.name}');")
        con.commit()
        self.db_get()
    
    def db_get(self):
        cur.execute(f"SELECT wid, gid, name FROM {self.db_table} WHERE name = '{self.name}'")
        self.wid, self.gid, self.name = cur.fetchone()

    def speak(self):
        sayit(self.name, slow=False)

    def spell(self):
        sayit(" ".join(self.name), slow=True)

    def __repr__(self) -> str:
        return f'{self.name}'


class Test:
    def __init__(self, user: User):
        self.db_table = 'test'
        self.datetime = datetime.now()
        self.user = user

    def start_test(self, wordgroup: Wordgroup):
        score_round = 0
        words = wordgroup.get_words()
        for word in words:
            os.system('clear')
            word.speak()
            guess = input('enter: ')
            self.db_insert(word, guess)
            if guess.lower() == word.name.lower():
                sayit(f'correct, well done {self.user.name}')
                score_round += 1
            else:
                sayit(f'incorrect')
                print(word.name)
                word.spell()
            input('press any key to continue')
        sayit(f'{score_round} out of {len(words)}')
    
    def db_insert(self, word: Word, guess: str):
        cur.execute(
            f"INSERT INTO {self.db_table} (uid, wid, username, guess, answer, correct, datetime)\n"
            f"VALUES('{self.user.uid}', '{word.wid}', '{self.user.username}', '{guess}', '{word.name}',"
            f"'{guess.lower() == word.name.lower()}', '{datetime.now()}');"
        )
        con.commit()


class Actions:

    def login(self):
        username = input('Username: ')
        self.user = User(username)

    def add_word_group(self):
        name = input('Enter wordgroup name: ')
        words = []
        while True:
            print('type x to exit input')
            words.append(input('Enter word: '))
            if words[-1] == 'x':
                break
        Wordgroup(name).add_words(words[:-1])

    def get_avalible_wordgroups(self):
        cur.execute(f"SELECT name FROM wordgroup")
        wordgroupnames = cur.fetchall()
        return [i[0] for i in wordgroupnames]

    def start_test(self):
        avalible_wordgroups = self.get_avalible_wordgroups()
        print(avalible_wordgroups)
        while True:
            i = input('Which wordgroup: ')
            if i in avalible_wordgroups:
                Test(self.user).start_test(Wordgroup(i))
                break
            else:
                'No wordgroup by that name'
    
    def print_report(self):
        sql = f"select * from test where username = '{self.user.username}'"
        print(pd.read_sql(sql, con))
        # pd.crosstab(a.guess, a.correct)
        input('press any key to exit')


def main():
    os.system('clear')
    print(f"{'-'*50}\nSpelling Game\n{'-'*50}\ns")
    action = Actions()
    action.login()

    menu_level1 = """1. exit
2. logout
3. change password
4. add word group
5. start test
6. play hangman
7. play word jumble
8. print report"""

    while True:
        os.system('clear')
        i = int(input(f'{menu_level1}\n\nEnter option: '))
        os.system('clear')
        if i == 1:
            exit()
        elif i == 2:
            action.login()
        elif i == 3:
            action.user.change_password()
        elif i == 4:
            action.add_word_group()
        elif i == 5:
            action.start_test()
        elif i == 6:
            pass
        elif i == 7:
            pass
        elif i == 8:
            action.print_report()
    

if __name__ == "__main__":
    main()
