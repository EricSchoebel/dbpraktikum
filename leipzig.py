#Vorbemerkung: postgres-DockerContainer must be up

# in terminal: pip install psycopg2
import psycopg2 #Psycopg is the most popular PostgreSQL database adapter for Python
import xml.etree.ElementTree as ET
import requests # NEU
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
tree_two = ET.parse("backend\data\leipzig_transformed.xml")
root_two = tree_two.getroot()

#Tabellen leeren vor erneutem Einfügen
"""
with connection.cursor() as cleaner2:
    cleaner2.execute("DELETE FROM Produkt_Kategorie; DELETE FROM Kategorie; DELETE FROM Produkt;")
connection.commit()
"""

with connection.cursor() as cursor_lpz:
    for item in root_two:
        #print(item.attrib)
        produktart = item.get('pgroup')
        pid = item.get('asin')
        #hier vielleicht noch ein if check -> siehe meine Fehlermeldung, das waere was für die Fehlerdatei

        verkaufsrang = item.get('salesrank')
        if len(verkaufsrang) == 0: #bei leerem String, muss ich fuer SQL eine NULLwert geben
            verkaufsrang = None

        image_url = item.get('picture')
        if len(image_url)>1: #checkt ob da ueberhaupt sowas wie URL drin ist
            response = requests.get(image_url) #downloadet das Bild via requests-Package
            image_data = response.content # psycopg2.Binary(image_data)  dann später als value fuer die sql-query


        if produktart == 'Music':
            for punkt in item: # "punkt" ist ein Tag (also inhaltlicher Punkt), wegens Namensgleichheit nicht "tag"
                if punkt.tag == 'title':
                    titel = punkt.text
                elif punkt.tag == 'labels':
                    labels = [label.get('name') for label in punkt.findall('label')] # ".get('')" weil es Attribut "name" in Untertag <label> ist
                elif punkt.tag == 'releasedate':
                    erscheinungsdatum = punkt.text
                elif punkt.tag == 'tracks':
                    titles = [track.text for track in punkt.findall('title')] # ".text" weil es gibt immer Untertag <title> mit Text -> Titel
                elif punkt.tag == 'artists':
                    artists = [artist.get('name') for artist in punkt.findall('artist')]
            cursor_lpz.execute(
                "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                (pid, titel, None, verkaufsrang, psycopg2.Binary(image_data), pid)  # Rating errechnet sich ja aus Rezensionen
            )




            #if item.get('title') =="In a Pig's Eye: Reflections on the Police State Re":
             #   print(item.get('pgroup'))


        elif produktart == 'DVD':
            pass

        elif produktart == 'Book':
            pass


#so kommst an attribute:  item.get('pgroup')
#so kommst an tag: inhaltspunkt.tag


# Commit the changes and close the connection
connection.commit()
connection.close()


