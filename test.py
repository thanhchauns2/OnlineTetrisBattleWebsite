import sqlite3

# Kết nối tới tệp tin SQLite
conn = sqlite3.connect('db.sqlite3')

# Tạo đối tượng cursor để thực hiện truy vấn
cursor = conn.cursor()

# Thực hiện truy vấn SELECT đơn giản
cursor.execute("SELECT * FROM auth_user")

# Lấy kết quả của truy vấn
result = cursor.fetchall()

# In kết quả
for row in result:
    print(row)

# Đóng kết nối và cursor
cursor.close()
conn.close()
