import sqlite3

command = input('command: ')

con = sqlite3.connect('../data/track_metadata.db')


def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute(command)
    print(cursorObj.fetchall())

sql_fetch(con)
