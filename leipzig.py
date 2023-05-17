#Vorbemerkung: postgres-DockerContainer must be up

# in terminal: pip install psycopg2
import psycopg2 #Psycopg is the most popular PostgreSQL database adapter for Python
import xml.etree.ElementTree as ET
import requests # NEU
import traceback # NEU
#import os
from SQL_drop_create import sql_drop_tables, sql_creates

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

with connection.cursor() as cleaner2: #nutzt vorgefertigte SQL-Skripte
    cleaner2.execute(sql_drop_tables)
    cleaner2.execute(sql_creates)
connection.commit()

kuenstler_id = 0
autor_id = 0
beteiligten_id = 0
filialen_id = 0

#Allgemeine Struktur fuer ein Item: I) spezifische Infos rausziehen , II) direkt in jeweilige Tabellen reinschreiben
with connection.cursor() as cursor_lpz:

    #Filialen einfuegen
    cursor_lpz.execute(
        "INSERT INTO Filiale (FID, Filialname) SELECT %s, %s "
        + "WHERE NOT EXISTS (SELECT 1 FROM Filiale where FID = %s);",
            (1, "Leipzig", 1)
    )
    cursor_lpz.execute(
        "INSERT INTO Filiale (FID, Filialname) SELECT %s, %s "
        + "WHERE NOT EXISTS (SELECT 1 FROM Filiale where FID = %s);",
        (2, "Dresden", 2)
    )
    connection.commit()



    for item in root_two:
        try:
            #print(item.attrib)
            produktart = item.get('pgroup')
            pid = item.get('asin')
            #hier vielleicht noch ein if check -> siehe meine Fehlermeldung, das waere was für die Fehlerdatei
            #if pid is not None:   #um zu sehen wo man ist
            #    print(pid)

            verkaufsrang = item.get('salesrank')
            if len(verkaufsrang) == 0: #bei leerem String, muss ich fuer SQL eine NULLwert geben
                verkaufsrang = None

            image_url = item.get('picture')
            if len(image_url)>0: #checkt ob da ueberhaupt sowas wie URL drin ist
                response = requests.get(image_url) #downloadet das Bild via requests-Package
                image_data = response.content # psycopg2.Binary(image_data)  dann später als value fuer die sql-query
                bild = psycopg2.Binary(image_data)
            else:
                bild = None


            if produktart == 'Music':
                kuenstler_total = []
                for punkt in item: # "punkt" ist ein Tag (also inhaltlicher Punkt), wegens Namensgleichheit nicht "tag"
                    if punkt.tag == 'title':
                        titel = punkt.text
                    elif punkt.tag == 'labels':
                        labels = [label.get('name') for label in punkt.findall('label')] # ".get('')" weil es Attribut "name" in Untertag <label> ist
                        longest_label = max(labels, key=len, default=None) #nur laengstes Label (mit meisten Infos) erhalten und None-Handling
                    elif punkt.tag == 'musicspec':
                        erscheinungsdatum_roh = [releasedate.text for releasedate in punkt.findall('releasedate')]
                        if erscheinungsdatum_roh is None:
                            erscheinungsdatum = None  # Or provide a default value or expression if needed
                        else:
                            erscheinungsdatum = erscheinungsdatum_roh[0]
                        #erscheinungsdatum = str(erscheinungsdatum_roh[0]) #ohenhin bloss einelementige Liste
                        print(erscheinungsdatum)
                    elif punkt.tag == 'tracks':
                        titles = [track.text for track in punkt.findall('title')] # ".text" weil es gibt immer Untertag <title> mit Text -> Titel
                    elif punkt.tag == 'artists':
                        artists = [artist.get('name') for artist in punkt.findall('artist')]
                        kuenstler_total.extend(artists)
                    elif punkt.tag == 'creators':
                        creators = [creator.get('name') for creator in punkt.findall('creator')]
                        kuenstler_total.extend(creators)
                    #FALSCH if len(kuenstler_total) == 0:
                    #    kuenstler_total = None


                cursor_lpz.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                    (pid, titel, None, verkaufsrang, bild, pid)  # Rating errechnet sich ja aus Rezensionen
                )
                connection.commit()

                cursor_lpz.execute(
                    "INSERT INTO CD (PID, Label, Erscheinungsdatum) SELECT %s, %s,"
                    +"CASE WHEN %s IS NULL THEN NULL ELSE to_date(%s, 'YYYY-MM-DD') END "
                    + "WHERE NOT EXISTS (SELECT 1 FROM CD where PID = %s);",
                    (pid, longest_label, erscheinungsdatum, erscheinungsdatum, pid)
                )
                connection.commit()

                #kuenstler sind entgegen der reinen Uebersetzung sowohl artists als auch creators
                for kuenstlername in kuenstler_total: #pro Kuenstler in KuenstlerTabelle UND CD_KuenstlerTabelle einfuegen (wegen ID)
                    kuenstler_id = kuenstler_id + 1
                    cursor_lpz.execute( #KuenstlerID ist nicht SERIAL, weil ich brauche in der Nutzung mehrmals die gleiche
                        "INSERT INTO Kuenstler (KuenstlerID, Kuenstlername) SELECT %s, %s "
                        + "WHERE NOT EXISTS (SELECT 1 FROM Kuenstler where Kuenstlername = %s);",
                        (kuenstler_id, kuenstlername, kuenstlername)
                    )
                    connection.commit()

                    cursor_lpz.execute(
                        "INSERT INTO CD_Kuenstler (PID, KuenstlerID) SELECT %s, %s "
                        + "WHERE NOT EXISTS (SELECT 1 FROM CD_Kuenstler where PID = %s AND KuenstlerID = %s);",
                        (pid, kuenstler_id, pid, kuenstler_id)
                    )
                    connection.commit()

                for track in titles:
                    cursor_lpz.execute(
                        "INSERT INTO Titel (PID, Titelname) SELECT %s, %s "
                        + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s AND Titelname = %s);",
                        (pid, track, pid, track)
                    )
                    connection.commit()

                '''
                #IN BEARBEITUNG:
                cursor_lpz.execute(
                    "INSERT INTO Angebot (PID, FID, Preis, Zustandsnummer, Menge) SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                    (pid, titel, None, verkaufsrang, bild, pid)  
                )
                connection.commit()
                '''






                #if item.get('title') =="In a Pig's Eye: Reflections on the Police State Re":
                 #   print(item.get('pgroup'))


            elif produktart == 'DVD':
                pass

            elif produktart == 'Book':
                pass

        except psycopg2.Error as error: # Fehlernachricht in einer Tabelle loggen
            connection.rollback()
            #error_message = str(error)  #kurze error message fuer Tabelle

            # lange error message fuer Tabelle; ohne Anfang der Fehlermeldung, der immer gleich ist
            traceback_string = str(traceback.format_exc())
            start_index = traceback_string.find("psycopg2.errors.") + len("psycopg2.errors.")
            error_message = (traceback_string[start_index:]).lstrip().replace('\n', ' ')   #lstrip() entfernt Anfangsleerzeichen

            with connection.cursor() as error_cursor:
                error_cursor.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)", (error_message,))
                connection.commit()
            print("Error:", error_message)  # Fehler in Console
            #traceback.print_exc() #ausfuerhlicher Fehler
            continue #mit naechstem Item weitermachen


#so kommst an attribute:  item.get('pgroup')
#so kommst an tag: inhaltspunkt.tag


# Commit the changes and close the connection
connection.commit()
connection.close()


