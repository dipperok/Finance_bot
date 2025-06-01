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
    
    def get_currency(self, user_name):
        self.cursor.execute(f"SELECT currency FROM users WHERE user_name = ?", (user_name,))
        result = self.cursor.fetchone()
        return result

    def add_record(self, user_name, operation, value, category):
        """Создать запись о расходе/доходе (-/+) с использованием user_id"""
        self.cursor.execute("SELECT user_id FROM users WHERE user_name = ?", (user_name,))
        result = self.cursor.fetchone()
        
        if not result:
            raise ValueError(f"Пользователь '{user_name}' не найден в таблице users.")
        user_id = result[0]
        
        self.cursor.execute(
            "INSERT INTO users_data (user_id, operation, sum, category) VALUES (?, ?, ?, ?)",
            (user_id, operation, value, category))
        self.conn.commit()


    def get_all_user_stat(self, user_name, first_date, second_date):
        pass
    
    def get_expence_user_stat(self, user_name, first_date, second_date):
        pass
    
    def get_profit_user_stat(self, user_name, first_date, second_date):
        pass

    def close(self):
        self.conn.close()
  
  
if __name__ == "__main__":
    bd = BotDB('db.sqlite')