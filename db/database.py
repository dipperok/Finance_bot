import sqlite3
from datetime import datetime, timedelta
from typing import Tuple, Dict, Union

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


    def get_all_user_stat(self, user_name: str, first_date: str, last_date: str) -> Union[Tuple[int, int, Dict[str, int]], None]:
        def parse_date_range(first_date: str, last_date: str) -> Tuple[str, str]:
            def parse_single(date_str: str, is_start: bool) -> str:
                parts = date_str.strip().split('.')
                if len(parts) == 2:  # формат "мм.гггг"
                    month, year = int(parts[0]), int(parts[1])
                    if is_start:
                        dt = datetime(year, month, 1)
                    else:
                        if month == 12:
                            dt = datetime(year + 1, 1, 1) - timedelta(days=1)
                        else:
                            dt = datetime(year, month + 1, 1) - timedelta(days=1)
                elif len(parts) == 3:  # формат "дд.мм.гггг"
                    day, month, year = map(int, parts)
                    dt = datetime(year, month, day)
                else:
                    raise ValueError("Неверный формат даты")
                return dt.strftime('%Y-%m-%d')

            return parse_single(first_date, True), parse_single(last_date, False)

        try:
            date_start, date_end = parse_date_range(first_date, last_date)
        except ValueError as e:
            print("Ошибка в формате даты:", e)
            return None

        # Получаем user_id по user_name
        self.cursor.execute("SELECT user_id FROM users WHERE user_name = ?", (user_name,))
        result = self.cursor.fetchone()
        if not result:
            print("Пользователь не найден.")
            return None
        user_id = result[0]

        # Получаем сумму "+" и "-" операций
        self.cursor.execute("""
            SELECT operation, SUM(sum)
            FROM users_data
            WHERE user_id = ?
              AND date(date_add) BETWEEN ? AND ?
            GROUP BY operation
        """, (user_id, date_start, date_end))

        sum_plus = 0
        sum_minus = 0
        for op, total in self.cursor.fetchall():
            if op == "+":
                sum_plus = total or 0
            elif op == "-":
                sum_minus = total or 0

        # Получаем суммы по категориям
        self.cursor.execute("""
            SELECT category, SUM(sum)
            FROM users_data
            WHERE user_id = ?
              AND date(date_add) BETWEEN ? AND ?
            GROUP BY category
        """, (user_id, date_start, date_end))

        category_totals = {row[0]: row[1] for row in self.cursor.fetchall()}

        return sum_plus, sum_minus, category_totals
    
    def get_expence_user_stat(self, user_name, first_date, second_date):
        pass
    
    def get_profit_user_stat(self, user_name, first_date, second_date):
        pass

    def close(self):
        self.conn.close()
  
  
if __name__ == "__main__":
    db = BotDB('db.sqlite')
    plus, minus, categories = db.get_all_user_stat('dipperok', '06.2025', '06.2025')
    print(plus, minus, categories)