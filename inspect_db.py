import sqlite3
import os
path = os.path.join(os.getcwd(), 'test.db')
print('db exists:', os.path.exists(path), 'path=', path)
if os.path.exists(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print('tables=', cur.fetchall())
        cur.execute('PRAGMA table_info(users)')
        print('users columns=', cur.fetchall())
        cur.execute('SELECT id,email,role,created_at FROM users')
        rows = cur.fetchall()
        print('rows count=', len(rows))
        for r in rows:
            print(r)
    except Exception as e:
        print('ERROR', e)
    finally:
        conn.close()
