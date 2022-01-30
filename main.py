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

    def print_progress_report(self):
        sql = f"select * from test where username = '{self.username}'"
        print(pd.read_sql(sql, con))
        # pd.crosstab(a.guess, a.correct)
        input('press any key to exit')

    def __repr__(self) -> str:
        return f'{self.name}'


class Wordgroup:
    def __init__(self, name: str=None):
        self.db_table = 'wordgroup'
        self.gid: int = None
        self.name: str = None
        self.words: list = [Word]

    def create_wordgroup(self, name: str):
        """create a new wordgroup and insert it to the database"""
        assert self.db_check_exists(name) is False
        self.name = name
        self.db_insert()
        self.db_get()

    def load_wordgroup(self, name: str):
        """load an existing word, fetches attributes from database"""
        assert self.db_check_exists(name)
        self.name = name
        self.db_get()
        return self
    
    def db_check_exists(self, name: str) -> bool:
        """checks whether word already exists in the database"""
        cur.execute(f"SELECT EXISTS (SELECT * FROM {self.db_table} WHERE name = '{name}')")
        return cur.fetchone()[0] == 1
    
    def db_insert(self):
        """inserts Wordgroup object metadata into the database"""
        cur.execute(f"INSERT INTO {self.db_table} (name) VALUES('{self.name}');")
        con.commit()
    
    def db_get(self):
        """gets Wordgroup object metadata from the database"""
        cur.execute(f"SELECT gid, name FROM {self.db_table} WHERE name = '{self.name}'")
        self.gid, self.name = cur.fetchone()
    
    def add_words(self, words: list = [str]):
        """save wordgroup words from database, generate Word object and append to self.words list"""
        self.words = [Word().create_word(word, self) for word in words]
    
    def load_words(self):
        """load wordgroup words from database, generate Word objects and append to self.words list"""
        cur.execute(
            f"select w.name\n"
            f"from {self.db_table} as wg\n"
            f"inner join word as w on w.gid = wg.gid\n"
            f"where wg.name = '{self.name}'"
        )
        self.words = [Word().load_word(word[0]) for word in cur.fetchall()]

    def __repr__(self) -> str:
        return f'{self.name} {self.words}'


class Word:
    def __init__(self, name: str=None):
        self.db_table: str = 'word'
        self.wid: int = None
        self.name: str = None
        self.wordgroup: Wordgroup = None

    def create_word(self, name: str, wordgroup: Wordgroup):
        """create a new word and insert it to the database"""
        assert self.db_check_exists(name) is False
        self.name = name
        self.wordgroup = wordgroup
        self.db_insert()
        self.db_get()

    def load_word(self, name: str):
        """load an existing word, fetches attributes from database"""
        assert self.db_check_exists(name)
        self.name = name
        self.db_get()
        return self
    
    def db_check_exists(self, name: str) -> bool:
        """checks whether word already exists in the database"""
        cur.execute(f"SELECT EXISTS (SELECT * FROM {self.db_table} WHERE name = '{name}')")
        return cur.fetchone()[0] == 1
    
    def db_insert(self):
        """inserts Word object metadata into the database"""
        cur.execute(f"INSERT INTO {self.db_table} (gid, name) VALUES('{self.wordgroup.gid}', '{self.name}');")
        con.commit()
        self.db_get()
    
    def db_get(self):
        """gets Word object metadata from the database"""
        cur.execute(f"SELECT wid, gid, name FROM {self.db_table} WHERE name = '{self.name}'")
        self.wid, self.gid, self.name = cur.fetchone()

    def speak(self):
        """audibly speaks the word"""
        sayit(self.name, slow=False)

    def spell(self):
        """audibly spells the word"""
        sayit(" ".join(self.name), slow=True)

    def __repr__(self) -> str:
        return f'{self.name}'


class Test:
    def __init__(self, user: User):
        self.db_table = 'test'
        self.datetime = datetime.now()
        self.user = user

    def get_avalible_wordgroups(self):
        cur.execute(f"SELECT name FROM wordgroup")
        wordgroupnames = cur.fetchall()
        return [i[0] for i in wordgroupnames]

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


def main():

    active_user = None
    
    os.system('clear')
    username = input('Username: ')
    active_user = User(username)

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
            active_user = User(input('Username: '))
        elif i == 3:
            active_user.change_password()
        elif i == 4:
            wordgroup = Wordgroup()
            wordgroup.create_wordgroup()
            wordgroup.add_words()
        elif i == 5:
            Actions.start_test()
        elif i == 6:
            pass
        elif i == 7:
            pass
        elif i == 8:
            active_user.print_progress_report()
    

if __name__ == "__main__":
    main()
