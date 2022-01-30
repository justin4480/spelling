import sqlite3

con = sqlite3.connect('my-test.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS user;')
cur.execute('DROP TABLE IF EXISTS wordgroup;')
cur.execute('DROP TABLE IF EXISTS word;')
cur.execute('DROP TABLE IF EXISTS test;')

cur.execute("""
    CREATE TABLE IF NOT EXISTS user (
        uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        name TEXT,
        password TEXT
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS wordgroup (
        gid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS word (
        wid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        gid INTERGER,
        name TEXT
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS test (
        tid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        uid INTERGER,
        wid INTERGER,
        username TEXT,
        guess TEXT,
        answer TEXT,
        correct INTERGER,
        datetime TEXT
    );
""")

con.commit()
con.close()