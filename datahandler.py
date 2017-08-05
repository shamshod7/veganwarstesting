import psycopg2
import os
from urllib.parse import urlparse

url = urlparse(os.environ['DATABASE_URL'])


def get_player(chat_id, username, first_name):

    if username is not None:
        db = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
        cursor = db.cursor()
        cursor.execute('SELECT name FROM players WHERE id = %s;', (chat_id,))
        data = cursor.fetchone()
        if data is None:
            cursor.execute('INSERT INTO players(id, games_played, games_won, name, username)VALUES (%s,%s,%s,N%s,%s)', (chat_id, 0, 0, first_name, '@' + username))
        else:
            print(data[0])
        db.commit()
        db.close()
    else:
        pass


def get_games(chat_id):
    db = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT games_played, games_won FROM players WHERE id = %s', (chat_id,))
    data = cursor.fetchone()
    db.close()
    if data is None:
        return None
    else:
        return data


def add_played_games(chat_id, game=1):
    db = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT games_played FROM players WHERE id = %s', (chat_id,))
    data = cursor.fetchone()
    games = int(data[0])
    games += game
    cursor.execute('UPDATE players SET games_played = %s WHERE id = %s', (games,chat_id))
    db.commit()
    db.close()


def getallplayers():
    db = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    db.row_factory = lambda cursor, row: row[0]
    cursor = db.cursor()
    ids = cursor.execute('SELECT id FROM players').fetchall()
    db.close()
    return ids


def add_won_games(chat_id, game=1):
    db = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT games_won FROM players WHERE id = %s', (chat_id,))
    data = cursor.fetchone()
    games = int(data[0])
    games += game
    cursor.execute('UPDATE players SET games_won = %s WHERE id = %s', (games, chat_id))
    db.commit()
    db.close()


def get_dataname(chat_id):
    db = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT name FROM players WHERE id = %s', (chat_id,))
    data = cursor.fetchone()
    db.close()
    return data[0]




def get_current(chat_id):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT current_weapon, current_items, current_skills FROM players WHERE id = %s', (chat_id,))
    data = cursor.fetchone()
    db.close()
    return data

def change_weapon(cid, weapon_name):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('UPDATE players SET current_weapon = N%s WHERE id = %s', (weapon_name, cid))
    db.commit()
    db.close()

def add_item(cid, item_id):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT current_items FROM players WHERE id = %s', (cid,))
    data = list(cursor.fetchone())
    if data[0] is None:
        data[0] = item_id
    elif len(data[0].split(',')) > 1:
        return False
    else:
        if data[0] == '':
            data[0] = item_id
        else:
            data[0] = data[0] + ',' + item_id
        while data[0] != '':
            if data[0][-1] != ',':
                break
            data[0] = data[0][:-1]
            if data[0] == '':
                data[0] = None
                break
    if data[0] is None:
        cursor.execute('UPDATE players SET current_items = %s WHERE id = %s', (None, cid))
    else:
        cursor.execute('UPDATE players SET current_items = N%s WHERE id = %s', (data[0], cid))
    db.commit()
    db.close()
    return True

def delete_item(cid, item_id):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT current_items FROM players WHERE id = %s', (cid,))
    data = list(cursor.fetchone())
    if data[0] is None:
        return False
    else:
        data[0] = data[0].replace(item_id, '')
        if data[0][-1] == ',':
            data[0] = data[0][:-1]
        if data[0][0] == ',':
            data[0] = data[0][:1]
        if data[0] == '':
            data[0] = None
    if data[0] is None:
        cursor.execute('UPDATE players SET current_items = %s WHERE id = %s', (None, cid))
    else:
        cursor.execute('UPDATE players SET current_items = N%s WHERE id = %s', (data[0], cid))
    db.commit()
    db.close()
    return True

def add_skill(cid, skill_name):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT current_skills FROM players WHERE id = %s', (cid,))
    data = list(cursor.fetchone())
    if data[0] is None:
        data[0] = skill_name
    elif len(data[0].split(',')) > 1:
        return False
    else:
        if data[0] == '':
            data[0] = skill_name
        else:
            data[0] = data[0] + ',' + skill_name
        while data[0] != '':
            if data[0][-1] != ',':
                break
            data[0] = data[0][:-1]
            if data[0] == '':
                data[0] = None
                break
    if data[0] is None:
        cursor.execute('UPDATE players SET current_skills = %s WHERE id = %s', (None, cid))
    else:
        cursor.execute('UPDATE players SET current_skills = N%s WHERE id = %s', (data[0], cid))
    db.commit()
    db.close()
    return True

def add_unique_weapon(username, weapon_name):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT unique_weapon FROM players WHERE username = %s', (username,))
    data = list(cursor.fetchone())
    if data[0] is None:
        data[0] = weapon_name
    else:
        if data[0] == '':
            data[0] = weapon_name
        else:
            weapons = data[0].split(',')
            if weapon_name not in weapons:
                data[0] = data[0] + ',' + weapon_name
            else:
                return False
        while data[0] != '':
            if data[0][-1] != ',':
                break
            data[0] = data[0][:-1]
            if data[0] == '':
                data[0] = None
                break
    cursor.execute('UPDATE players SET unique_weapon = %s WHERE username = %s', (data[0], username))
    db.commit()
    db.close()
    return True

def delete_unique_weapon(username, weapon_name):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT unique_weapon FROM players WHERE username = %s', (username,))
    data = list(cursor.fetchone())
    if data[0] is None:
        pass
    else:
        if weapon_name in data[0]:
            data[0] = data[0].replace(weapon_name, '')
            if data[0][-1] == ',':
                data[0] = data[0][:-1]
            if data[0][0] == ',':
                data[0] = data[0][:1]
            if data[0] == '':
                data[0] = None
    cursor.execute('UPDATE players SET unique_weapon = %s WHERE username = %s', (data[0], username))
    db.commit()
    db.close()
    return True

def get_unique(chat_id):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT unique_weapon, unique_items, unique_skills FROM players WHERE id = %s', (chat_id,))
    data = cursor.fetchone()
    db.close()
    return data

def delete_skill(cid, skill_name):
    db = psycopg2.connect(
        "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    cursor = db.cursor()
    cursor.execute('SELECT current_skills FROM players WHERE id = %s', (cid,))
    data = list(cursor.fetchone())
    if data[0] is None:
        return False
    else:
        data[0] = data[0].replace(skill_name, '')
        if data[0][-1] == ',':
            data[0] = data[0][:-1]
        if data[0][0] == ',':
            data[0] = data[0][:1]
        if data[0] == '':
            data[0] = None
    if data[0] is None:
        cursor.execute('UPDATE players SET current_skills = %s WHERE id = %s', (None, cid))
    else:
        cursor.execute('UPDATE players SET current_skills = N%s WHERE id = %s', (data[0], cid))
    db.commit()
    db.close()
    return True
