import sqlite3

class DBManager:
    def __init__(self, wiki_db='wiki_pages.db', user_db='user_preferences.db'):
        self.conn1 = sqlite3.connect(wiki_db)
        self.cursor1 = self.conn1.cursor()
        self.create_wiki_table()

        self.conn2 = sqlite3.connect(user_db)
        self.cursor2 = self.conn2.cursor()
        self.create_user_table()

    def create_wiki_table(self):
        self.cursor1.execute('''CREATE TABLE IF NOT EXISTS wiki_pages
                               (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
        self.conn1.commit()

    def create_user_table(self):
        self.cursor2.execute('''CREATE TABLE IF NOT EXISTS user_preferences
                                (id INTEGER PRIMARY KEY, user_id INTEGER, language TEXT, article_length TEXT)''')
        self.conn2.commit()

    def insert_page(self, title, content):
        self.cursor1.execute('''INSERT INTO wiki_pages (title, content) VALUES (?, ?)''', (title, content))
        self.conn1.commit()

    def get_page(self, title):
        self.cursor1.execute('''SELECT * FROM wiki_pages WHERE title = ?''', (title,))
        return self.cursor1.fetchone()
    #user
    def save_user_preferences(self, user_id, language, article_length):
        self.cursor2.execute('''INSERT INTO user_preferences (user_id, language, article_length) VALUES (?, ?, ?)''',
                              (user_id, language, article_length))
        self.conn2.commit()

    def get_user_preferences(self, user_id):
        self.cursor2.execute('''SELECT * FROM user_preferences WHERE user_id = ?''', (user_id,))
        return self.cursor2.fetchone()

    def close_connections(self):
        self.conn1.close()
        self.conn2.close()

if __name__ == '__main__':
    manager = DBManager()