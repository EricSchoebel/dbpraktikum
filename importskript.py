#Vorbemerkung: postgres-DockerContainer must be up

# in terminal: pip install psycopg2
import psycopg2 #Psycopg is the most popular PostgreSQL database adapter for Python
import xml.etree.ElementTree as ET
#import os

try:
    connection = psycopg2.connect(
        host="localhost",
        port="6432", # hier 6432 weil ich die Portbindung geändert hatte
        database="dbprak_postgres",
        user="dbprak_postgres",
        password="dbprak_postgres"
    )

except psycopg2.Error as error:
    print("Error connecting to PostgreSQL:", error)


# Etree-package initialisieren
tree = ET.parse("backend\data\categories.xml")
root = tree.getroot()



#fuehrende Zahl zeigt an, ob es Haupt- oder Unterkategorie ist
#hauptkategorien beginnen mit 1
#unterkategorien beginnen mit 2

id_zaehler = 0

#rekursive Funktionsdefinition (für einen Hauptkategoriestrang)
def grabeTiefer(oberkategorie, ober_id):
    for unter in oberkategorie:

        if unter.tag == 'item':
            # item_tag = unter.tag
            # dann unter.text into Produkt (braucht es später nicht mehr), aber (Stand 13.5.) ist ja Produkttabelle noch nicht gefüllt:
            cursor.execute(
                "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                +"WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                (unter.text, None, None, None, None, unter.text)  # hier schreibst Variablen die rein sollen
            )

            cursor.execute(
                "INSERT INTO Produkt_Kategorie (KatID, PID) SELECT %s, %s "
                +"WHERE NOT EXISTS (SELECT 1 FROM Produkt_Kategorie WHERE KatID= %s AND PID = %s);",
                (ober_id, unter.text, ober_id, unter.text)  # hier schreibst Variablen die rein sollen
            )

        if unter.tag == 'category':
            global id_zaehler
            id_zaehler = id_zaehler + 1
            new_id = int("2" + ( str(id_zaehler)) )
            # katgorie reinschreiben in tabelle kategorie
            # weitergraben
            cursor.execute(
                "INSERT INTO Kategorie (KatID, Kategoriename, Oberkategorie) VALUES (%s, %s, %s);",
                (new_id, unter.text, ober_id)
            )
            grabeTiefer(unter, new_id)  # jetzt ist Unter die neue Oberkategorie



#Tabellen leeren vor erneutem Einfügen
with connection.cursor() as cleaner:
    cleaner.execute("DELETE FROM Produkt_Kategorie; DELETE FROM Kategorie; DELETE FROM Produkt;")
connection.commit()


#Einfügen
with connection.cursor() as cursor:
    for hauptkategorie in root:
        id_zaehler = id_zaehler + 1  #hier musst nicht "global setzen weil es keine Funktion ist
        #print(hauptkategorie.text)
        actual_id = int("1"+str(id_zaehler))
        #print(id_zaehler)
        cursor.execute(
             "INSERT INTO Kategorie (KatID, Kategoriename, Oberkategorie) VALUES (%s, %s, %s);",
                          (actual_id, hauptkategorie.text, None) #hier schreibst Variablen die rein sollen
                       )
        grabeTiefer(hauptkategorie, actual_id)


# Commit the changes and close the connection
connection.commit()
connection.close()



#musste zuvor erstellt werden:
"""
CREATE TABLE Kategorie (
  KatID INT PRIMARY KEY,
  Kategoriename VARCHAR(255),
  Oberkategorie INT,
  FOREIGN KEY (Oberkategorie) REFERENCES Kategorie(KatID)
);

CREATE TABLE Produkt_Kategorie (
  KatID INT,
  PID INT,
  PRIMARY KEY (KatID, PID),
  FOREIGN KEY (KatID) REFERENCES Kategorie(KatID),
  FOREIGN KEY (PID) REFERENCES Produkt(PID)
);

CREATE TABLE Produkt (
  PID INT PRIMARY KEY,
  Titel VARCHAR(255),
  Rating DECIMAL(2,1),
  Verkaufsrang INT,
  Bild VARCHAR(255)
);

"""




#current_directory = os.getcwd()
#print("Current working directory:", current_directory)

#if __name__ == '__main__':
#    print(Hi)

# Define the folder path
#folder_path = "backend/data"