#Creation base de donnee

import mysql.connector
	db_connection = mysql.connector.connect(
  	host="localhost",
  	user="root",
  	passwd="password"
    )



# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor()
# executing cursor with execute method and pass SQL query
db_cursor.execute("CREATE DATABASE Inventaire PJT")

db_cursor.execute("CREATE TABLE Materiel(id_materiel INT PRIMARY KEY, date_garantie TEXT, date_dernier_entretient TEXT, derniere_localisation TEXT) ")










#get database table
for table in db_cursor:
	print(table)
    
