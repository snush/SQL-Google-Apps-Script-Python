import csv, sqlite3

conn = sqlite3.connect(''':memory:''')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE table (id, name);''')

with open('data.csv','rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'], i['name']) for i in dr]

cursor.executemany('''INSERT INTO table (id, name) VALUES (?, ?);''', to_db)
conn.commit()

# 1 вариант
cursor.execute('''DELETE FROM table t1 
               WHERE EXISTS (SELECT 1 FROM table t2 WHERE t2.id < t1.id and t1.name = t2.name);''')

# 2 вариант
cursor.execute('''DELETE FROM table 
                WHERE id NOT IN (SELECT max(id) FROM table GROUP BY name HAVING count(id) > 1;''')

conn.commit()
conn.close()