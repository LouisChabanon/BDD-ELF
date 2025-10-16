#Creation base de donnee
#Pour githup
#Dès qu'il y a un changement, on renseigne le commit et on fait push



import mysql.connector
db_connection = mysql.connector.connect(
  	host="localhost",
  	user="root",
  	passwd="password"
    )



db_cursor = db_connection.cursor()


#Suppression de l'ancienne base et création d'une nouvelle table
db_cursor.execute("DROP DATABASE IF EXISTS Inventaire_PJT")
db_cursor.execute("CREATE DATABASE Inventaire_PJT")
db_connection.close()



import mysql.connector
db_connection = mysql.connector.connect(
  	host="localhost",
  	user="root",
  	passwd="password",
    database="Inventaire_PJT"
    )


db_cursor.execute("CREATE TABLE Materiel(id_materiel INT PRIMARY KEY, date_garantie TEXT, date_dernier_entretient TEXT, derniere_localisation TEXT) ")
db_cursor.execute("CREATE TABLE Emprunt(id_emprunt INT PRIMARY KEY, moti TEXT, date_emprunt TEXT)")
db_cursor.execute("CREATE TABLE Matos(nom_materiel TEXT PRIMARY KEY, photo_materiel TEXT, frequence_entretient TEXT)")
db_cursor.execute("CREATE TABLE Rangement(lieu_rangement TEXT PRIMARY KEY)")
db_cursor.execute("CREATE TABLE Kit(nom_kit TEXT PRIMARY KEY)")
db_cursor.execute("CREATE TABLE Historique(date_rendu TEXT PRIMARY KEY, FOREIGN KEY REFERENCE Materiel(id_materiel))")
db_cursor.execute("CREATE TABLE Notice(notice_materiel TEXT PRIMARY KEY)")
db_cursor.execute("CREATE TABLE Personnel(id_personnel INT PRIMARY KEY, mail TEXT, type_personnel TEXT, nom TEXT, prenom TEXT)")
db_cursor.execute("CREATE TABLE Reservation(date_reservation TEXT, FOREIGN KEY REFERENCE Personnel(id_personnel), FOREIGN KEY Materiel(id_materiel))")










#get database table
for table in db_cursor:
	print(table)
    
