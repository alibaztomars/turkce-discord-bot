import sqlite3
import json

class Database:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                data TEXT
            )
        ''')
        self.conn.commit()

    def get_user_data(self, user_id):
        self.cursor.execute('SELECT data FROM users WHERE id = ?', (user_id,))
        result = self.cursor.fetchone()
        if result:
            return json.loads(result[0])
        else:
            return None

    def save_user_data(self, user_id, data):
        data_str = json.dumps(data)
        self.cursor.execute('''
            INSERT INTO users (id, data) VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET data=excluded.data
        ''', (user_id, data_str))
        self.conn.commit()

    def user_exists(self, user_id):
        self.cursor.execute('SELECT 1 FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone() is not None

    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def create_new_user(self, user_id):
        self.cursor.execute('INSERT INTO users (id, data) VALUES (?, ?)', (user_id, json.dumps({})))
        self.conn.commit()

