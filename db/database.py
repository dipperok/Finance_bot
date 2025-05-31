import sqlite3

class BotDB:
	def __init__(self, db_file):
		self.conn = sqlite3.connect(db_file)
		self.cursor = self.conn.cursor()

	def user_exists(self, user_name):
		result = self.cursor.execute(f"SELECT user_name FROM users WHERE user_name = ?", (user_name,))
		return bool(len(result.fetchall()))

	def add_record(self, user_name, operation, value, category):
		"""Создать запись о расходе/доходе (-/+)"""
		self.cursor.execute(f"INSERT INTO users_data (user_name, operation, value, category) VALUES (?, ?, ?, ?)",
			(user_name, operation, value, category))
		return self.conn.commit()



	def close(self):
		self.conn.close()
  
  
if __name__ == "__main__":
    bd = BotDB('db.sqlite')
    print(bd.user_exists('dipperok'))