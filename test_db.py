import psycopg2

conn = psycopg2.connect(
    dbname="finance_bot",
    user="finance_user",
    password="finance_pass",
    host="192.168.1.207",
    port="5432"
)

cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM users_data;")
print(cur.fetchone())

cur.close()
conn.close()
