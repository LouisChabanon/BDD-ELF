#Creation base de donnee
#Pour githup
#Dès qu'il y a un changement, on renseigne le commit et on fait push


import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()
db_connection = mysql.connector.connect(
  	host=os.getenv("DB_HOST"),
	port=os.getenv("DB_PORT"),
  	user=os.getenv("DB_USER"),
  	passwd=os.getenv("DB_PASSWORD")
    )



db_cursor = db_connection.cursor()


#Suppression de l'ancienne base et création d'une nouvelle table
db_cursor.execute("DROP DATABASE IF EXISTS Inventaire_PJT")
db_cursor.execute("CREATE DATABASE Inventaire_PJT")
db_connection.close()




db_connection = mysql.connector.connect(
  	host=os.getenv("DB_HOST"),
	port=os.getenv("DB_PORT"),
  	user=os.getenv("DB_USER"),
  	passwd=os.getenv("DB_PASSWORD"),
	database=os.getenv("DB_NAME")
    )

db_cursor = db_connection.cursor()

db_cursor.execute("CREATE TABLE Materiel(id_materiel INT PRIMARY KEY, date_garantie TEXT, date_dernier_entretient TEXT, derniere_localisation TEXT) ")
db_cursor.execute("CREATE TABLE Emprunt(id_emprunt INT PRIMARY KEY, motif TEXT, date_emprunt TEXT)")
db_cursor.execute("CREATE TABLE Matos(nom_materiel VARCHAR(100) PRIMARY KEY, photo_materiel TEXT, frequence_entretient TEXT)")
db_cursor.execute("CREATE TABLE Rangement(lieu_rangement VARCHAR(100) PRIMARY KEY)")
db_cursor.execute("CREATE TABLE Kit(nom_kit VARCHAR(100) PRIMARY KEY)")

db_cursor.execute("CREATE TABLE Historique(date_rendu VARCHAR(100) PRIMARY KEY, id_materiel INT, FOREIGN KEY (id_materiel) REFERENCES Materiel(id_materiel))")

db_cursor.execute("CREATE TABLE Notice(notice_materiel VARCHAR(100) PRIMARY KEY)")
db_cursor.execute("CREATE TABLE Personnel(id_personnel INT PRIMARY KEY, mail TEXT, type_personnel TEXT, nom TEXT, prenom TEXT)")
db_cursor.execute("CREATE TABLE Reservation(date_reservation TEXT, id_personnel INT, id_materiel INT, FOREIGN KEY (id_personnel) REFERENCES Personnel(id_personnel), FOREIGN KEY (id_materiel) REFERENCES Materiel(id_materiel))")










#get database table
for table in db_cursor:
	print(table)
    
