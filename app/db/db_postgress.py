import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Tuple, Dict, Union


class BotDBpg:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        """
        Подключение к PostgreSQL
        """
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    # ---------- Работа с пользователями ----------

    def user_exists(self, user_name: str) -> bool:
        self.cursor.execute("SELECT user_name FROM users WHERE user_name = %s", (user_name,))
        return bool(self.cursor.fetchall())

    def get_first_message_status(self, user_name: str) -> bool:
        self.cursor.execute("SELECT fst_msg_status FROM users WHERE user_name = %s", (user_name,))
        result = self.cursor.fetchone()

        if not result:
            return False

        if result["fst_msg_status"]:
            return True
        else:
            self.cursor.execute("UPDATE users SET fst_msg_status = 1 WHERE user_name = %s", (user_name,))
            self.conn.commit()
            return False

    def get_categories(self, user_name: str):
        self.cursor.execute("SELECT categories FROM users WHERE user_name = %s", (user_name,))
        result = self.cursor.fetchone()
        if result and result["categories"]:
            categories_str = result["categories"]
            return [c.strip() for c in categories_str.split(",") if c.strip()]
        return []

    def get_currency(self, user_name: str):
        self.cursor.execute("SELECT currence FROM users WHERE user_name = %s", (user_name,))
        result = self.cursor.fetchone()
        return result["currence"] if result else None

    # ---------- Работа с записями ----------

    def add_record(self, user_name: str, operation: str, value: float, category: str):
        """Создать запись о расходе/доходе (-/+) с использованием user_id"""
        self.cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        result = self.cursor.fetchone()

        if not result:
            raise ValueError(f"Пользователь '{user_name}' не найден в таблице users.")

        user_id = result["user_id"]

        self.cursor.execute("""
            INSERT INTO users_data (user_ud, operation, sum, category, date_add)
            VALUES (%s, %s, %s, %s, NOW())
        """, (user_id, operation, value, category))
        self.conn.commit()

    def get_all_period(self, user_name: str):
        self.cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        user_id_result = self.cursor.fetchone()

        if not user_id_result:
            print(f"Пользователь '{user_name}' не найден.")
            return None

        user_id = user_id_result["user_id"]

        self.cursor.execute("SELECT MIN(date_add) AS first_date, MAX(date_add) AS last_date FROM users_data WHERE user_ud = %s", (user_id,))
        result = self.cursor.fetchone()

        if not result or not result["first_date"] or not result["last_date"]:
            print(f"Для пользователя '{user_name}' нет записей в таблице users_data.")
            return None

        first_date = result["first_date"].strftime("%d.%m.%Y")
        last_date = result["last_date"].strftime("%d.%m.%Y")

        return first_date, last_date

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

        self.cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        result = self.cursor.fetchone()
        if not result:
            print("Пользователь не найден.")
            return None
        user_id = result["user_id"]

        # Сумма по операциям
        self.cursor.execute("""
            SELECT operation, SUM(sum) AS total
            FROM users_data
            WHERE user_ud = %s
              AND date_add::date BETWEEN %s AND %s
            GROUP BY operation
        """, (user_id, date_start, date_end))

        sum_plus = 0
        sum_minus = 0
        for row in self.cursor.fetchall():
            if row["operation"] == "+":
                sum_plus = int(row["total"] or 0)
            elif row["operation"] == "-":
                sum_minus = int(row["total"] or 0)

        # Суммы по категориям расходов
        self.cursor.execute("""
            SELECT category, SUM(sum) AS total
            FROM users_data
            WHERE user_ud = %s
              AND date_add::date BETWEEN %s AND %s
              AND operation = '-'
            GROUP BY category
        """, (user_id, date_start, date_end))

        category_totals = {row["category"]: int(row["total"]) for row in self.cursor.fetchall()}

        return sum_plus, sum_minus, category_totals

    def del_last_record(self, user_name: str) -> bool:
        self.cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        user_id_result = self.cursor.fetchone()
        if not user_id_result:
            return False

        user_id = user_id_result["user_id"]

        self.cursor.execute("SELECT id FROM users_data WHERE user_ud = %s ORDER BY id DESC LIMIT 1", (user_id,))
        last_record = self.cursor.fetchone()

        if not last_record:
            return False

        last_id = last_record["id"]

        self.cursor.execute("DELETE FROM users_data WHERE id = %s", (last_id,))
        self.conn.commit()
        return True

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    db = BotDBpg(
        dbname="finance_bot",
        user="finance_user",
        password="finance_pass",
        host="localhost",
        port=5432
    )
    plus, minus, categories = db.get_all_user_stat('dipperok', '07.2025', '07.2025')
    print(plus, minus, categories)
    db.close()
