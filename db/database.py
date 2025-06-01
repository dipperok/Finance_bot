import sqlite3

class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_name):
        result = self.cursor.execute(f"SELECT user_name FROM users WHERE user_name = ?", (user_name,))
        return bool(len(result.fetchall()))

    def get_categories(self, user_name):
        self.cursor.execute(f"SELECT categories FROM users WHERE user_name = ?", (user_name,))
        result = self.cursor.fetchone()
        if result and result[0]:
            categories_str = result[0]
            return [category.strip() for category in categories_str.split(",") if category.strip()]
        return []

    def add_record(self, user_name, operation, value, category):
        """Создать запись о расходе/доходе (-/+)"""
        self.cursor.execute(f"INSERT INTO users_data (user_name, operation, value, category) VALUES (?, ?, ?, ?)",
        (user_name, operation, value, category))
        return self.conn.commit()


    def close(self):
        self.conn.close()
  
  
if __name__ == "__main__":
    bd = BotDB('db.sqlite')