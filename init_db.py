import sqlite3

def init_db():
    conn = sqlite3.connect('mood.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mood_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            text TEXT NOT NULL,
            mood TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call the function once
if __name__ == '__main__':
    init_db()