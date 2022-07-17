import logging
import sqlite3

from flask import g

from src import config
from src import exceptions


def get_db():
    db = getattr(g, 'db', None)
    if not db:
        db = g.db = sqlite3.connect(config.DB_PATH)
    return db


def close_connection(*args, **kwargs):
    db = getattr(g, 'db', None)
    if db:
        db.close()


def get_user_pwd(username: str):
    cur = get_db().cursor()
    pwd = cur.execute(
        'select password from Users where username = ?', [username]
    ).fetchone()
    cur.close()
    if not pwd:
        raise exceptions.UserNotFound
    return pwd[0]


def save_to_db(user: str, file_hash: str, file_path: str):
    conn = get_db()
    cur = conn.cursor()

    user_id = cur.execute(
        'select id from Users where username = ?', [user]
    ).fetchone()[0]

    try:
        cur.execute('begin')
        cur.execute(
            'insert into UserFiles (user_id, hash, path) values (?, ?, ?)',
            [user_id, file_hash, file_path]
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        logging.exception(e)
        conn.rollback()
        raise exceptions.FileAlreadyExists
    except sqlite3.Error as e:
        logging.exception(e)
        conn.rollback()
        raise e
    finally:
        cur.close()


def remove_from_db(user: str, file_hash: str):
    conn = get_db()
    cur = conn.cursor()

    user_id = cur.execute(
        'select id from Users where username = ?', [user]
    ).fetchone()[0]

    try:
        user_file_exists = cur.execute(
            'select count(*) from UserFiles where user_id = ? and hash = ?',
            [user_id, file_hash]
        ).fetchone()[0]
        if not user_file_exists:
            raise exceptions.UserFileNotFound

        cur.execute(
            'delete from UserFiles where user_id = ? and hash = ?',
            [user_id, file_hash]
        )
        conn.commit()
    except sqlite3.Error as e:
        logging.exception(e)
        raise e
    finally:
        cur.close()
