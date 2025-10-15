import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()

# Run a query
cursor.execute("SELECT * FROM your_table;")

# Fetch and print results
for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
conn.close()
