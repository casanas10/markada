import mysql.connector as mysql
import config

#unpack dictionary credentials
conn = mysql.connect(**config.dbConfig)

cursor = conn.cursor()

try:
    cursor.execute("CREATE DATABASE {}".format("articles"))
except:
    print("Failed to create DB")

conn.close()