import sqlite3
import json

def update_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the 'users' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if cursor.fetchone() is None:
        # If the table does not exist, create it
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                data TEXT
            )
        ''')
    else:
        # If the table exists, check if it has the 'data' column
        cursor.execute("PRAGMA table_info(users);")
        columns = [column[1] for column in cursor.fetchall()]
        if 'data' not in columns:
            # If the 'data' column does not exist, add it
            cursor.execute("ALTER TABLE users ADD COLUMN data TEXT;")

    # Update existing user data to include level and xp
    cursor.execute("SELECT id, data FROM users")
    users = cursor.fetchall()
    for user_id, data in users:
        user_data = json.loads(data)
        if 'level' not in user_data:
            user_data['level'] = 1
        if 'xp' not in user_data:
            user_data['xp'] = 0
        cursor.execute('''
            UPDATE users
            SET data = ?
            WHERE id = ?
        ''', (json.dumps(user_data), user_id))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Run the update function
update_database()
