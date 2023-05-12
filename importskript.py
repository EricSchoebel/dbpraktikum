#Vorbemerkung: postgres-DockerContainer must be up

# in terminal: pip install psycopg2
import psycopg2 #Psycopg is the most popular PostgreSQL database adapter for Python
import xml.etree.ElementTree as ET
import os

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




#current_directory = os.getcwd()
#print("Current working directory:", current_directory)


# Parse the XML file
tree = ET.parse("backend\data\categories.xml")
root = tree.getroot()

#hauptkategorien beginnen mit 1
#unterkategorien beginnen mit 2
#hauptkategorien = []

#fuehrende zahl sagt dir ob es haupt oder unterkategorie ist
haupt_prefix = "1"
unter_prefix = "2"
id_zaehler = 0
boolean_hauptkat = False # der ist nur dazu da, um zu zeigen ob ich gerade von einer Hauptkategorie komme


def grabeTiefer(oberkategorie, ober_id, boolean_hauptkat):
    for unter in oberkategorie:

        prefix = ""
        if (boolean_hauptkat):
            prefix = haupt_prefix
        else:
            prefix = unter_prefix

        if unter.tag == 'item':
            # item_tag = unter.tag
            # dann unter.text into Produkt (braucht es später nicht mehr):
            cursor.execute(
                "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) VALUES (%s, %s, %s, %s, %s)",
                (unter.text, None, None, None, None)  # hier schreibst Variablen die rein sollen
            )

            cursor.execute(
                "INSERT INTO Produkt_Kategorie (KatID, PID) VALUES (%s, %s)",
                (ober_id, unter.text)  # hier schreibst Variablen die rein sollen
            )

        # den boolean_hauptkat will ich mitgebn damit ich die neue id für den falll ordentlich bilden kann und keine übertragprobleme kriege

        if unter.tag == 'category':
            global id_zaehler
            id_zaehler = id_zaehler + 1
            new_id = int(prefix + ( str(int(str(ober_id)[1:])+1)) )
            # katgorie reinschreiben in tabelle kategorie
            # weitergraben
            cursor.execute(
                "INSERT INTO Kategorie (KatID, Kategoriename, Oberkategorie) VALUES (%s, %s, %s)",
                (new_id, unter.text, ober_id)
            )
            grabeTiefer(unter, new_id, False)  # jetzt ist Unter die neue Oberkategorie





with connection.cursor() as cursor:
    for hauptkategorie in root:
        boolean_hauptkat = True
        id_zaehler = id_zaehler + 1  #hier musst nicht "global setzen weil es keine Funktion ist
        print(hauptkategorie.text)
        actual_id = int(haupt_prefix+str(id_zaehler))
        print(id_zaehler)
        cursor.execute(
             "INSERT INTO Kategorie (KatID, Kategoriename, Oberkategorie) VALUES (%s, %s, %s)",
                          (actual_id, hauptkategorie.text, None) #hier schreibst Variablen die rein sollen
                       )


        grabeTiefer(hauptkategorie, actual_id, boolean_hauptkat)


        #for unterkategorieOne in hauptkategorie:





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


#print(ET.tostring(root, encoding='utf8').decode('utf8'))

#print([elem.tag for elem in root.iter()])









#for category, item in categories_and_items:
#    print(f"Category: {category}, Item: {item}")



# Function to insert categories recursively
#def insert_categories(categories, parent_id=None):
#    with connection.cursor() as cursor:
#        for category in categories:
#            category_name = category.text.strip()
#            cursor.execute(
#                "INSERT INTO Kategorie (Kategoriename, Oberkategorie) VALUES (%s, %s) RETURNING KatID",
#                (category_name, parent_id)
#            )
#            category_id = cursor.fetchone()[0]
#            if category.findall('category'):
#                insert_categories(category.findall('category'), category_id)

# Start inserting categories from the root level
#insert_categories(root.findall('category'))




# Commit the changes and close the connection
connection.commit()









# Perform database operations here

#sql_statement = "SELECT 12"
#with connection:
#    with connection.cursor() as cursor:
#        cursor.execute(sql_statement)
#        rows = cursor.fetchall()

#for child in root:
#    print(child.tag, child.attrib)



# cursor = connection.cursor()
# cursor.execute("SELECT * FROM friendship") # friendship war die Beispieltabelle, die ich angelegt hatte
# rows = cursor.fetchall()
#for row in rows:
#    print(row)

#cursor.close()
connection.close()





#if __name__ == '__main__':
#    print(Hi)

# Define the folder path
#folder_path = "backend/data"