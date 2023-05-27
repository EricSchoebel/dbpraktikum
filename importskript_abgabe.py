#Vorbemerkung: postgres-DockerContainer must be up

# in terminal: pip install psycopg2
import psycopg2 #Psycopg is the most popular PostgreSQL database adapter for Python
import xml.etree.ElementTree as ET
import requests # NEU
import traceback # NEU
#import os
from SQL_drop_create import sql_drop_tables, sql_creates
import decimal
import csv
import html
from thefuzz import fuzz #Fuzzy-Suche, basiert auf Levenshtein-Distanz / Editierdistanz

#Fuzzy-Matching
#Beispiel: in Daten gab es die Autoren "Andreas Fröhlich" und "Andreas Frhlich", wahrscheinlich diesselbe Person
#s1 = "Andreas Fröhlich"
#s2 = "Andreas Frhlich"
#print(fuzz.ratio(s1, s2)) #ergibt ratio (eine Art Aehnlichkeitsmaß) von 97  (100 waere exakt gleicher String)

# berechnet aehnlichkeitsratio (eine Art Aehnlichkeitsmaß, 100 waere exakt gleicher String)
def berechne_aehnlichkeitsratio(name1, name2):
    return fuzz.ratio(name1, name2)

#Input: pruefstring = Name oder aehnliches der auf fuzzy-Vorhandensein in DB ueberpueft werden soll
#       sqlstring = Abfrage zur relevanter Spalte
#       aehnlichkeitsratio-Grenzwert, wie gleich es sein muss um als fuzzy_matached zu gelten.
#               Grenzwert für jeweilige Tabelle und Attrbut durch Ausprobieren herausgefunden
#Rueckgabetuple gibt an ob fuzzy_matched und wenn True mit welchem Namen
def berechne_fuzzy_matched(pruefstring, sqlstring, grenzwert, speziellercursor) -> tuple[bool, str]:
    # Daten zur Ueberpruefung aus DB holen
    speziellercursor.execute(sqlstring)
    namen = speziellercursor.fetchall()

    fuzzy_matched = False
    matched_name = ""
    #gegenchecke alle in Tabellenspalte bereits vorhandenen Namen
    for name1 in namen:
            if name1 != pruefstring:
                aehnlichkeitsratio = berechne_aehnlichkeitsratio(name1[0], pruefstring)  # "[0]" weil es ja eig. Tupel ist
                if aehnlichkeitsratio > grenzwert and aehnlichkeitsratio<100:  # Grenzwert
                    # print(f"Aehnlichkeit zwischen {name1[0]} und {pruefstring}: {aehnlichkeitsratio}%")
                    fuzzy_matched = True
                    matched_name = name1[0]
    result_tuple = (fuzzy_matched, matched_name)
    return result_tuple



#falls ein Fuzzy-Match gefunden wurde, wird dessen ID gebraucht
def finde_ID_zu_matchend_name(sqlstring, speziellercursor):
    speziellercursor.execute(sqlstring)
    ID_tupel = speziellercursor.fetchone()
    return ID_tupel[0]


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

#----------LEIPZIG ANFANG--------------------

print("Verarbeite Leipzig-Daten...")

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
angebot_id_zaehler = 0


#Allgemeine Struktur fuer ein Item: I) spezifische Infos rausziehen , II) direkt in jeweilige Tabellen reinschreiben
with connection.cursor() as cursor_lpz:

    filialname_lpz = root_two.get('name')
    filial_lpz_strasse = root_two.get('street')
    filial_lpz_PLZ = root_two.get('zip')
    fid_lpz = 1

    #Filialen einfuegen
    cursor_lpz.execute(
        "INSERT INTO Filiale (FID, Filialname) SELECT %s, %s "
        + "WHERE NOT EXISTS (SELECT 1 FROM Filiale where FID = %s);",
            (fid_lpz, filialname_lpz, fid_lpz)
    )

    #Anschrift einfuegen, spaeter auch analog fuer Dresden
    cursor_lpz.execute(
        "INSERT INTO Anschrift (FID, Strasse, Hausnummer, PLZ) SELECT %s, %s, %s, %s "
        + "WHERE NOT EXISTS (SELECT 1 FROM Filiale where FID = %s);",
        (1, filial_lpz_strasse, None, filial_lpz_PLZ, 1)
    )
    connection.commit()

    #Checke alle Zustaende im gesamten Dokument fuer ZustandTabelle
    # (in LepzigXML gibt es nur 'new')
    states = set()
    for x in root_two.iter():
        if x.tag == "price":
            state = x.get("state")
            states.add(state)

    #ZustaendeTabelle befuellen
    for state in states:
        try:
            cursor_lpz.execute(
                "INSERT INTO Zustand (Beschreibung) VALUES (%s) ;",
                (state,) #WICHTIG: du musst Tupel übergeben, auch bei nur einer Wertuebergabe, deshalb ","
            )
            connection.commit()
        except psycopg2.Error as error: # Fehlernachricht in einer Tabelle loggen
            connection.rollback()
            #error_message = str(error)  #kurze error message fuer Tabelle

            # lange error message fuer Tabelle; ohne Anfang der Fehlermeldung, der immer gleich ist
            traceback_string = str(traceback.format_exc())
            start_index = traceback_string.find("psycopg2.errors.") + len("psycopg2.errors.")
            error_message = (traceback_string[start_index:]).lstrip().replace('\n', ' ')   #lstrip() entfernt Anfangsleerzeichen
            error_message = "ERROR: " + error_message

            with connection.cursor() as error_cursor:
                error_cursor.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)", (error_message,))
                connection.commit()
            print("Error:", error_message)  # Fehler in Console
            #traceback.print_exc() #ausfuerhlicher Fehler
            continue




    for item in root_two:
        try:

            #die folgenden Infos sind bei Leipzig bei jeder Produktart gleich UND sind in Item-Tag zu finden
            #print(item.attrib)
            produktart = item.get('pgroup')
            pid = item.get('asin')

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


            if (produktart == 'Music') or (produktart == 'Book' and (str(pid)).startswith('B')):

                # WARNING bzgl. (wahrscheinl.) Hoerbuechern, z.B.: PID "B000AMF7X8"
                if ( produktart == 'Book' and (str(pid)).startswith('B') ):
                    eigene_fehlernachricht = 'WARNING: Speicherung erfolgt unter "CD", obwohl Produktart "Book" vorhanden.' \
                                             + ' Gründe wie PID sprechen für CD. Ggf. manuell überprüfen. Warning entstand bei: PID: ' + pid \
                                             + ', Produktart: ' + produktart
                    cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                       (eigene_fehlernachricht,))
                    connection.commit()
                    print(eigene_fehlernachricht)

                kuenstler_total = []
                for punkt in item: # "punkt" ist ein Tag (also inhaltlicher Punkt), wegens Namensgleichheit nicht "tag"
                    if punkt.tag == 'title':
                        titel = punkt.text
                    elif punkt.tag == 'price': #das ist zwar auch bei jeder Produktart das gleiche Vorgehen
                        multiplizierer = punkt.get('mult')
                        zustand = punkt.get('state')
                        currency = punkt.get('currency')
                        centpreis = punkt.text
                        if centpreis is not None and multiplizierer is not None:
                            europreis = decimal.Decimal(multiplizierer) * decimal.Decimal(centpreis)
                        else:
                            europreis = None

                        #Test, dass wirklich nur EUR-Preise
                        if (currency != 'EUR') and (len(currency)>0):
                            print("currency ist nicht null und nicht Euro: "+currency)
                            #tritt bei Music zweimal auf, aber das es "EUREUR" ist, kann man davon ausgehen, dass Euro gemeint war
                            eigene_fehlernachricht = 'WARNING: "currency" ist nicht "EUR" sondern "' + currency + '". ' \
                                                     + 'Datenbank nimmt EUR an. Warning entstand bei: PID: ' + pid \
                                                     + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                                 (eigene_fehlernachricht,))
                            connection.commit()


                    elif punkt.tag == 'labels':
                        labels = [label.get('name') for label in punkt.findall('label')] # ".get('')" weil es Attribut "name" in Untertag <label> ist
                        longest_label = max(labels, key=len, default=None) #nur laengstes Label (mit meisten Infos) erhalten und None-Handling
                    elif punkt.tag == 'musicspec':
                        erscheinungsdatum_roh = [releasedate.text for releasedate in punkt.findall('releasedate')]
                        if erscheinungsdatum_roh is None:
                            erscheinungsdatum = None  # Or provide a default value or expression if needed
                        else:
                            try:
                                erscheinungsdatum = erscheinungsdatum_roh[0]
                            except:
                                erscheinungsdatum = None
                        #erscheinungsdatum = str(erscheinungsdatum_roh[0]) #ohenhin bloss einelementige Liste
                        #print(erscheinungsdatum)
                    elif punkt.tag == 'tracks':
                        titles = [track.text for track in punkt.findall('title')] # ".text" weil es gibt immer Untertag <title> mit Text -> Titel
                    elif punkt.tag == 'artists':
                        artists = [artist.get('name') for artist in punkt.findall('artist')]
                        kuenstler_total.extend(artists)
                    elif punkt.tag == 'creators':
                        creators = [creator.get('name') for creator in punkt.findall('creator')]
                        kuenstler_total.extend(creators)

                    elif punkt.tag == 'similars':
                        # Liste von Tupeln mit Tupel: (aehnlich_pid, aehnlich_titel)
                        aehnliche_produkte_tupelliste = [ (sim_product.find('asin').text, sim_product.find('title').text)  #Liste von Tupeln
                                            for sim_product in punkt.findall('sim_product')]

                #Einschreiben in Tabellen
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

                # Retrieve the maximum kuenstler_id from the Kuenstler table
                cursor_lpz.execute("SELECT MAX(KuenstlerID) FROM Kuenstler;")
                max_kuenstler_id = cursor_lpz.fetchone()[0]
                #print("max_kuenstlerID:")
                #print(max_kuenstler_id)


                #kuenstler sind entgegen der reinen Uebersetzung sowohl artists als auch creators
                #Weitere Herausforderung war: wenn es den Kuenstlernamen schon gibt, dann keinen neuen Eintrag in Kuenstlertabelle machen,
                #sondern mit bestehender KuenstlerID die Verbindung in CD_Kuenstler machen
                # (hochzaehllogik musste man aufpassen)
                for kuenstlername in kuenstler_total:
                    names = kuenstlername.split("/") #weil manchmal in einem kuenstlernamen eig. mehrere mit "/" separiert reingechrieben

                    for name in names:
                        #print(name)
                        # Hole maximum kuenstler_id von KuenstlerTabelle
                        name = name.lstrip().rstrip() #fuehrende und endende Blanks loeschen fuer semantische Gleichheit
                        cursor_lpz.execute("SELECT MAX(KuenstlerID) FROM Kuenstler;")
                        max_kuenstler_id = cursor_lpz.fetchone()[0]

                        # setze initiale kuenstler_id auf maximumn kuenstler_id
                        if max_kuenstler_id is None:
                            kuenstler_id = 0
                        else:
                            kuenstler_id = max_kuenstler_id

                        cursor_lpz.execute(
                            "SELECT KuenstlerID FROM Kuenstler WHERE Kuenstlername = %s;",
                            (name,)
                        )
                        existing_kuenstler = cursor_lpz.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT kuenstlername FROM Kuenstler", 86, cursor_lpz)

                        if existing_kuenstler is not None:  #Fall: Kuenstlername gibt's schon in Kuenstler table
                            kuenstler_id = existing_kuenstler[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            #print(fuzzy_tuple)
                            sqlstring = "SELECT kuenstlerid FROM Kuenstler where kuenstlername='" + fuzzy_tuple[1] + "'"
                            kuenstler_id = finde_ID_zu_matchend_name(sqlstring, cursor_lpz)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(kuenstler_id) + ' .'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                                   (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                        else:  #Fall: Kuenstlernamen gibt es noch nicht in Kuenstler table, dann musst einen neuen Eintrag in Kuenstler Tabelle machen
                            kuenstler_id = kuenstler_id + 1
                            cursor_lpz.execute(
                                "INSERT INTO Kuenstler (KuenstlerID, Kuenstlername) VALUES (%s, %s)",
                                (kuenstler_id, name)
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
                        + "WHERE NOT EXISTS (SELECT 1 FROM Titel where PID = %s AND Titelname = %s);",
                        (pid, track, pid, track)
                    )
                    connection.commit()


            elif (produktart == 'Book') and not (str(pid)).startswith('B'):
                for punkt in item: # "punkt" ist ein Tag (also inhaltlicher Punkt), wegens Namensgleichheit nicht "tag"
                    if punkt.tag == 'title':
                        titel = punkt.text
                    elif punkt.tag == 'price': #das ist zwar auch bei jeder Produktart das gleiche Vorgehen
                        multiplizierer = punkt.get('mult')
                        zustand = punkt.get('state')
                        currency = punkt.get('currency')
                        centpreis = punkt.text
                        if centpreis is not None and multiplizierer is not None:
                            europreis = decimal.Decimal(multiplizierer) * decimal.Decimal(centpreis)
                        else:
                            europreis = None
                        # Test, dass wirklich nur EUR-Preise
                        if (currency != 'EUR') and (len(currency) > 0):
                            print("currency ist nicht null und nicht Euro: " + currency)
                            eigene_fehlernachricht = 'WARNING: "currency" ist nicht "EUR" sondern "' + currency + '". ' \
                                                     + 'Datenbank nimmt EUR an. Warning entstand bei: PID: ' + pid \
                                                     + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                                       (eigene_fehlernachricht,))
                            connection.commit()

                    elif punkt.tag == 'bookspec':
                        erscheinungsdatum_buch_roh = [publicationdate.get('date') for publicationdate in punkt.findall('publication')]
                        if erscheinungsdatum_buch_roh is None:
                            erscheinungsdatum_buch = None
                        else:
                            erscheinungsdatum_buch = erscheinungsdatum_buch_roh[0]

                        seitenzahl_roh = [page.text for page in punkt.findall('pages')]
                        if seitenzahl_roh is None:
                            seitenzahl = None
                        else:
                            seitenzahl = seitenzahl_roh[0]

                        isbn_roh = [nummer.get('val') for nummer in punkt.findall('isbn')]
                        if isbn_roh is None:
                            isbn = None
                        else:
                            isbn = isbn_roh[0]

                        binding_roh = [binding.text for binding in punkt.findall('binding')]
                        if binding_roh is None:
                            binding = None
                        else:
                            binding = binding_roh[0]

                        if binding == 'CD':
                            eigene_fehlernachricht = 'WARNING: Speicherung erfolgt unter "Buch", obwohl Binding "CD" vorhanden. Hinweis fuer ein potenzielles Hoerbuch,' \
                                                     + ' ggf. Änderungen vornehmen. Warning entstand bei: PID: ' + pid \
                                                     + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                    elif punkt.tag == 'publishers':
                        verlage = [publisher.get('name') for publisher in
                                  punkt.findall('publisher')]  # ".get('')" weil es Attribut "name" in Untertag <publisher> ist
                        longest_verlag = max(verlage, key=len,
                                            default=None)  # nur laengster Verlag (mit meisten Infos) erhalten und None-Handling

                    elif punkt.tag == 'authors':
                        authors = [author.get('name') for author in punkt.findall('author')]

                    elif punkt.tag == 'similars':
                        # Liste von Tupeln mit Tupel: (aehnlich_pid, aehnlich_titel)
                        aehnliche_produkte_tupelliste = [ (sim_product.find('asin').text, sim_product.find('title').text)  #Liste von Tupeln
                                            for sim_product in punkt.findall('sim_product')]

                    #nur fuer TrackCheck ob eventuell Hoerbuch:
                    elif punkt.tag == 'tracks':
                        titles = [track.text for track in punkt.findall('title')]


                cursor_lpz.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                    (pid, titel, None, verkaufsrang, bild, pid)  # Rating errechnet sich ja aus Rezensionen
                )
                connection.commit()

                cursor_lpz.execute(
                    "INSERT INTO Buch (PID, Seitenzahl, Erscheinungsdatum, isbn, verlag) SELECT %s, %s, "
                    + "CASE WHEN %s IS NULL THEN NULL ELSE to_date(%s, 'YYYY-MM-DD') END "
                    + ", %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Buch where PID = %s);",
                    (pid, seitenzahl, erscheinungsdatum_buch, erscheinungsdatum_buch, isbn, longest_verlag, pid)
                )
                connection.commit()
                #print(erscheinungsdatum_buch)

                #WARNING bzgl. (wahrscheinl.) Hoerbuechern
                if len(titles)>0:
                    eigene_fehlernachricht = 'WARNING: Speicherung erfolgt unter "Buch", obwohl Tracks vorhanden. Hinweis fuer ein potenzielles Hoerbuch,' \
                                             + ' ggf. Änderungen vornehmen. Warning entstand bei: PID: ' + pid \
                                             + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                    cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                       (eigene_fehlernachricht,))
                    connection.commit()
                    print(eigene_fehlernachricht)

                # Retrieve the maximum autor_id from the Autor table
                cursor_lpz.execute("SELECT MAX(AutorID) FROM Autor;")
                max_autor_id = cursor_lpz.fetchone()[0]

                # wenn es den Autornamen schon gibt, dann keinen neuen Eintrag in Autortabelle machen,
                # sondern mit bestehender AutorID die Verbindung in Buch_Autor machen
                # (hochzaehllogik musste man aufpassen)
                for autorname in authors:
                    names = autorname.split(
                        "/")  # falls in einem Autornamen eig. mehrere mit "/" separiert reingechrieben
    
                    for name in names:
                        # print(name)
                        # Hole maximum autor_id von AutorTabelle
                        name = name.lstrip().rstrip()
                        cursor_lpz.execute("SELECT MAX(AutorID) FROM Autor;")
                        connection.commit()
                        max_autor_id = cursor_lpz.fetchone()[0]
    
                        # setze initiale autor_id auf maximumn autor_id
                        if max_autor_id is None:
                            autor_id = 0
                        else:
                            autor_id = max_autor_id
    
                        cursor_lpz.execute(
                            "SELECT AutorID FROM Autor WHERE Autorname = %s;",
                            (name,)
                        )
                        connection.commit()
                        existing_autor = cursor_lpz.fetchone()

                        #--Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT autorname FROM Autor", 85, cursor_lpz)

                        if existing_autor is not None:  # Fall: Autorname gibt's schon in Autor table
                            autor_id = existing_autor[0]

                        #--Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT autorid FROM Autor where autorname='" + fuzzy_tuple[1] + "'"
                            autor_id = finde_ID_zu_matchend_name(sqlstring, cursor_lpz)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(autor_id) + ' .'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)
                            continue

                        else:  # Fall: Autorennamen gibt es noch nicht in Autor table, dann musst einen neuen Eintrag in Autor Tabelle machen
                            autor_id = autor_id + 1
                            cursor_lpz.execute(
                                "INSERT INTO Autor (AutorID, Autorname) VALUES (%s, %s)",
                                (autor_id, name)
                            )
                            connection.commit()
    
                        cursor_lpz.execute(
                            "INSERT INTO Buch_Autor (PID, AutorID) SELECT %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM Buch_Autor where PID = %s AND AutorID = %s);",
                            (pid, autor_id, pid, autor_id)
                        )
                        connection.commit()


            elif produktart == 'DVD':
                for punkt in item: # "punkt" ist ein Tag (also inhaltlicher Punkt), wegens Namensgleichheit nicht "tag"
                    if punkt.tag == 'title':
                        titel = punkt.text
                    elif punkt.tag == 'price': #das ist zwar auch bei jeder Produktart das gleiche Vorgehen
                        multiplizierer = punkt.get('mult')
                        zustand = punkt.get('state')
                        currency = punkt.get('currency')
                        centpreis = punkt.text
                        if centpreis is not None and multiplizierer is not None:
                            europreis = decimal.Decimal(multiplizierer) * decimal.Decimal(centpreis)
                        else:
                            europreis = None
                        # Test, dass wirklich nur EUR-Preise
                        if (currency != 'EUR') and (len(currency) > 0):
                            print("currency ist nicht null und nicht Euro: " + currency)
                            eigene_fehlernachricht = 'WARNING: "currency" ist nicht "EUR" sondern "' + currency + '". ' \
                                                     + 'Datenbank nimmt EUR an. Warning entstand bei: PID: ' + pid \
                                                     + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                                       (eigene_fehlernachricht,))
                            connection.commit()

                    elif punkt.tag == 'dvdspec':

                        #Erscheinungsdatum soll bei dvd nicht gespeichert werden lt. Aufgabenstellung, aber so wuerde es gehen:
                        #erscheinungsdatum_dvd_roh = [releasedate.text for releasedate in punkt.findall('releasedate')]
                        #if erscheinungsdatum_dvd_roh is None:
                        #    erscheinungsdatum_dvd = None
                        #else:
                        #    erscheinungsdatum_dvd = erscheinungsdatum_dvd_roh[0]

                        format_roh = [format.text for format in punkt.findall('format')]
                        if format_roh is None:
                            format = None
                        else:
                            format = format_roh[0]

                        regioncode_roh = [regioncode.text for regioncode in punkt.findall('regioncode')]
                        if regioncode_roh is None:
                            regioncode = None
                        else:
                            regioncode = regioncode_roh[0]

                        laufzeit_roh = [runningtime.text for runningtime in punkt.findall('runningtime')]
                        if laufzeit_roh is None:
                            laufzeit = None
                        else:
                            laufzeit = laufzeit_roh[0]

                    elif punkt.tag == 'actors':
                        actors = [actor.get('name') for actor in punkt.findall('actor')]

                    elif punkt.tag == 'creators':
                        creators = [creator.get('name') for creator in punkt.findall('creator')]

                    elif punkt.tag == 'directors':
                        directors = [director.get('name') for director in punkt.findall('director')]

                    elif punkt.tag == 'similars':
                        # Liste von Tupeln mit Tupel: (aehnlich_pid, aehnlich_titel)
                        aehnliche_produkte_tupelliste = [ (sim_product.find('asin').text, sim_product.find('title').text)  #Liste von Tupeln
                                            for sim_product in punkt.findall('sim_product')]

                cursor_lpz.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                    (pid, titel, None, verkaufsrang, bild, pid)  # Rating errechnet sich ja aus Rezensionen
                )
                connection.commit()

                cursor_lpz.execute(
                    "INSERT INTO DVD (PID, Format, Laufzeit, Regioncode) SELECT %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM DVD where PID = %s);",
                    (pid, format, laufzeit, regioncode, pid)
                )
                connection.commit()


                # Retrieve the maximum beteiligten_id from the DVD_Beteiligte table
                cursor_lpz.execute("SELECT MAX(BeteiligtenID) FROM DVD_Beteiligte;")
                max_beteiligten_id = cursor_lpz.fetchone()[0]

                # DVD_BeteiligteTabelle bezeichnet als BeteiligteTabelle im Folgenden
                # wenn es den Beteiligtennamen schon gibt, dann keinen neuen Eintrag in Beteiligtentabelle machen,
                # sondern mit bestehender BeteiligtenID die Verbindung in DVD_Beteiligungen (=  n:m-Tabelle) machen
                # Logik fuer actors, creators, directors analog, nur rolle unterscheidet sich in der DVD_Beteiligungen-Tabelle (d.h. in der n:m-Tabelle)
                for actorname in actors:
                    rolle = 'actor'
                    names = actorname.split(
                        "/")  # falls in einem Actornamen eig. mehrere mit "/" separiert reingechrieben

                    for name in names:
                        # print(name)
                        # Hole maximum beteiligten_id von BeteiligteTabelle
                        name = name.lstrip().rstrip()
                        cursor_lpz.execute("SELECT MAX(BeteiligtenID) FROM DVD_Beteiligte;")
                        max_beteiligten_id = cursor_lpz.fetchone()[0]

                        # setze initiale beteiligten_id auf maximumn beteiligten_id
                        if max_beteiligten_id is None:
                            beteiligten_id = 0
                        else:
                            beteiligten_id = max_beteiligten_id

                        cursor_lpz.execute(
                            "SELECT BeteiligtenID FROM DVD_Beteiligte WHERE Beteiligtenname = %s;",
                            (name,)
                        )
                        existing_beteiligter = cursor_lpz.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT beteiligtenname FROM dvd_beteiligte", 90, cursor_lpz)

                        if existing_beteiligter is not None:  # Fall: Beteiligtenname gibt's schon in BeteiligterTabelle
                            beteiligten_id = existing_beteiligter[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT BeteiligtenID FROM dvd_beteiligte where beteiligtenname='" + fuzzy_tuple[1] + "'"
                            beteiligten_id = finde_ID_zu_matchend_name(sqlstring, cursor_lpz)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(beteiligten_id) + ' .'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                                   (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                        else:  # Fall: Beteiligtennamen gibt es noch nicht in BeteiligteTabelle, dann musst einen neuen Eintrag in BeteiligtenTabelle machen
                            beteiligten_id = beteiligten_id + 1
                            cursor_lpz.execute(
                                "INSERT INTO DVD_Beteiligte (BeteiligtenID, Beteiligtenname) VALUES (%s, %s)",
                                (beteiligten_id, name)
                            )
                            connection.commit()

                        cursor_lpz.execute(
                            "INSERT INTO DVD_Beteiligungen (PID, BeteiligtenID, Rolle) SELECT %s, %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM DVD_Beteiligungen where PID = %s AND BeteiligtenID = %s AND Rolle = %s);",
                            (pid, beteiligten_id, rolle, pid, beteiligten_id, rolle)
                        )
                        connection.commit()

                for creatorname in creators:
                    rolle = 'creator'
                    names = creatorname.split(
                        "/")

                    for name in names:
                        # print(name)
                        # Hole maximum beteiligten_id von BeteiligteTabelle
                        name = name.lstrip().rstrip()
                        cursor_lpz.execute("SELECT MAX(BeteiligtenID) FROM DVD_Beteiligte;")
                        max_beteiligten_id = cursor_lpz.fetchone()[0]

                        # setze initiale beteiligten_id auf maximumn beteiligten_id
                        if max_beteiligten_id is None:
                            beteiligten_id = 0
                        else:
                            beteiligten_id = max_beteiligten_id

                        cursor_lpz.execute(
                            "SELECT BeteiligtenID FROM DVD_Beteiligte WHERE Beteiligtenname = %s;",
                            (name,)
                        )
                        existing_beteiligter = cursor_lpz.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT beteiligtenname FROM dvd_beteiligte", 90,
                                                             cursor_lpz)

                        if existing_beteiligter is not None:  # Fall: Beteiligtenname gibt's schon in BeteiligterTabelle
                            beteiligten_id = existing_beteiligter[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT BeteiligtenID FROM dvd_beteiligte where beteiligtenname='" + \
                                        fuzzy_tuple[1] + "'"
                            beteiligten_id = finde_ID_zu_matchend_name(sqlstring, cursor_lpz)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(beteiligten_id) + ' .'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                        else:  # Fall: Beteiligtennamen gibt es noch nicht in BeteiligteTabelle, dann musst einen neuen Eintrag in BeteiligtenTabelle machen
                            beteiligten_id = beteiligten_id + 1
                            cursor_lpz.execute(
                                "INSERT INTO DVD_Beteiligte (BeteiligtenID, Beteiligtenname) VALUES (%s, %s)",
                                (beteiligten_id, name)
                            )
                            connection.commit()

                        cursor_lpz.execute(
                            "INSERT INTO DVD_Beteiligungen (PID, BeteiligtenID, Rolle) SELECT %s, %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM DVD_Beteiligungen where PID = %s AND BeteiligtenID = %s AND Rolle = %s);",
                            (pid, beteiligten_id, rolle, pid, beteiligten_id, rolle)
                        )
                        connection.commit()

                for directorname in directors:
                    rolle = 'director'
                    names = directorname.split(
                        "/")

                    for name in names:
                        # print(name)
                        # Hole maximum beteiligten_id von BeteiligteTabelle
                        name = name.lstrip().rstrip()
                        cursor_lpz.execute("SELECT MAX(BeteiligtenID) FROM DVD_Beteiligte;")
                        max_beteiligten_id = cursor_lpz.fetchone()[0]

                        # setze initiale beteiligten_id auf maximumn beteiligten_id
                        if max_beteiligten_id is None:
                            beteiligten_id = 0
                        else:
                            beteiligten_id = max_beteiligten_id

                        cursor_lpz.execute(
                            "SELECT BeteiligtenID FROM DVD_Beteiligte WHERE Beteiligtenname = %s;",
                            (name,)
                        )
                        existing_beteiligter = cursor_lpz.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT beteiligtenname FROM dvd_beteiligte", 90,
                                                             cursor_lpz)

                        if existing_beteiligter is not None:  # Fall: Beteiligtenname gibt's schon in BeteiligterTabelle
                            beteiligten_id = existing_beteiligter[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT BeteiligtenID FROM dvd_beteiligte where beteiligtenname='" + \
                                        fuzzy_tuple[1] + "'"
                            beteiligten_id = finde_ID_zu_matchend_name(sqlstring, cursor_lpz)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(beteiligten_id) + ' .'
                            cursor_lpz.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                        else:  # Fall: Beteiligtennamen gibt es noch nicht in BeteiligteTabelle, dann musst einen neuen Eintrag in BeteiligtenTabelle machen
                            beteiligten_id = beteiligten_id + 1
                            cursor_lpz.execute(
                                "INSERT INTO DVD_Beteiligte (BeteiligtenID, Beteiligtenname) VALUES (%s, %s)",
                                (beteiligten_id, name)
                            )
                            connection.commit()

                        cursor_lpz.execute(
                            "INSERT INTO DVD_Beteiligungen (PID, BeteiligtenID, Rolle) SELECT %s, %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM DVD_Beteiligungen where PID = %s AND BeteiligtenID = %s AND Rolle = %s);",
                            (pid, beteiligten_id, rolle, pid, beteiligten_id, rolle)
                        )
                        connection.commit()













            #INSERTs, die fuer alle Produktarten gleich:

            # Suche Zustandsnummer fuer gegebenen Zustand
            # eig. fuer alle Produktarten gleich
            cursor_lpz.execute(
                "SELECT Zustandsnummer FROM Zustand WHERE Beschreibung = %s;",
                (zustand,)
            )
            zustandsnummer_aktuell = cursor_lpz.fetchone()

            # Hole maximum AngebotsID von AngebotTabelle (Analog zu Kuenstlertabelle in der Hinsicht)
            cursor_lpz.execute("SELECT MAX(AngebotsID) FROM Angebot;")
            max_angebot_id_zaehler = cursor_lpz.fetchone()[0]

            # setze initiale angebot_id_zaehler auf maximumn angebot_id_zaehler
            if max_angebot_id_zaehler is None:
                angebot_id_zaehler = 0
            else:
                angebot_id_zaehler = max_angebot_id_zaehler

            # Idee: Check ob es das Angebot in dieser Form schon gibt
            #  -> Wenn ja, dann "Menge" um eins hoch (uber UPDATE in SQL)
            #  -> Wenn nein, dann neues Tupel (mit neuer AngebotsID) in AngebotTabelle

            # Check ob es das Angebot in dieser Form schon gibt
            cursor_lpz.execute(
                "SELECT AngebotsID, Menge FROM Angebot WHERE PID = %s AND FID = %s AND Preis = %s AND Zustandsnummer = %s;",
                (pid, fid_lpz, europreis, zustandsnummer_aktuell)
            )
            existing_offer = cursor_lpz.fetchone()

            # Fall: Angebot existiert bereits
            if existing_offer is not None:
                angebots_id = existing_offer[0]
                menge = existing_offer[1] + 1

                # Aktualisiere die Menge im vorhandenen Angebot
                cursor_lpz.execute(
                    "UPDATE Angebot SET Menge = %s WHERE AngebotsID = %s;",
                    (menge, angebots_id)
                )
                connection.commit()

            # Fall: Angebot existiert noch nicht
            else:
                angebot_id_zaehler = angebot_id_zaehler + 1

                # Neues Tupel in AngebotTabelle einfügen
                cursor_lpz.execute(
                    "INSERT INTO Angebot (AngebotsID, PID, FID, Preis, Zustandsnummer, Menge) "
                    "VALUES (%s, %s, %s, %s, %s, %s);",
                    (angebot_id_zaehler, pid, fid_lpz, europreis, zustandsnummer_aktuell, 1)
                    # Annahme: Menge startet bei 1
                )
                connection.commit()

            # AehnlichkeitTabelle befuellen (fuer alle Arten gleich)
            # (lexikographisch) kleinere PID ist immer PID1
            # aehnliche_produkte_tupelliste  nutzen
            # (aehnlich_pid, aehnlich_titel)
            # aehnliche_produkte_tupelliste
            for tupel in aehnliche_produkte_tupelliste:
                #wenn das AehnlichkeitsProdukt noch nicht in ProduktTabelle, dann noch da eintragen
                cursor_lpz.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) "
                    + "SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt WHERE PID = %s);",
                    (tupel[0], tupel[1], None, None, None, tupel[0])
                )
                connection.commit()

                kleiner = 0
                groesser = 0
                if str(pid) < str(tupel[0]):
                    kleiner = pid
                    groesser = tupel[0]
                elif str(tupel[0]) < str(pid):
                    kleiner = tupel[0]
                    groesser = pid

                if kleiner != groesser:
                    cursor_lpz.execute(
                        "INSERT INTO Aehnlichkeit (PID1, PID2) "
                        + "SELECT %s, %s "
                        + "WHERE NOT EXISTS (SELECT 1 FROM Aehnlichkeit WHERE PID1 = %s and PID2 = %s);",
                        (kleiner, groesser, kleiner, groesser)
                    )
                    connection.commit()


        except psycopg2.Error as error: # Fehlernachricht in einer Tabelle loggen
            connection.rollback()
            #error_message = str(error)  #kurze error message fuer Tabelle

            # lange error message fuer Tabelle; ohne Anfang der Fehlermeldung, der immer gleich ist
            traceback_string = str(traceback.format_exc())
            start_index = traceback_string.find("psycopg2.errors.") + len("psycopg2.errors.")
            error_message = (traceback_string[start_index:]).lstrip().replace('\n', ' ')   #lstrip() entfernt Anfangsleerzeichen
            error_message = "ERROR: " + error_message

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

#cursor_lpz.close() #Leipzig cursor schliessen um ihn nicht aus Versehen zu verwenden

#----------LEIPZIG ENDE--------------------







#--------------DRESDEN ANFANG---------

print("Verarbeite Dresden-Daten...")

# Etree-package initialisieren
tree_three = ET.parse("backend\data\dresden.xml")
root_three = tree_three.getroot()

# Tabellen leeren vor erneutem Einfügen

# DRESDEN BESONDERHEIT: Leipzig Filiale steht ja schon drin
#die ganzen id-Zaehler laufen ja von Leipzig weiter
#kuenstler_id = 0
#autor_id = 0
#beteiligten_id = 0
#filialen_id = 0
#angebot_id_zaehler = 0

# Allgemeine Struktur fuer ein Item: I) spezifische Infos rausziehen , II) direkt in jeweilige Tabellen reinschreiben
with connection.cursor() as cursor_dresden:
    filialname_dresden = root_three.get('name')
    filial_dresden_strasse = root_three.get('street')
    filial_dresden_PLZ = root_three.get('zip')
    fid_dresden = 2

    # Filialen einfuegen
    # DRESDEN BESONDERHEIT: Leipzig Filiale steht ja schon drin
    cursor_dresden.execute(
        "INSERT INTO Filiale (FID, Filialname) SELECT %s, %s "
        + "WHERE NOT EXISTS (SELECT 1 FROM Filiale where FID = %s);",
        (fid_dresden, filialname_dresden, fid_dresden)
    )
    connection.commit()

    # DRESDEN BESONDERHEIT: Leipzig Filiale steht ja schon drin
    cursor_dresden.execute(
        "INSERT INTO Anschrift (FID, Strasse, Hausnummer, PLZ) SELECT %s, %s, %s, %s "
        + "WHERE NOT EXISTS (SELECT 1 FROM Filiale where FID = %s);",
        (2, filial_dresden_strasse, None, filial_dresden_PLZ, 2)
    )
    connection.commit()

    # Checke alle Zustaende im gesamten Dokument fuer ZustandTabelle
    # (in LepzigXML gibt es nur 'new')
    states = set()
    for x in root_three.iter():
        if x.tag == "price":
            state = x.get("state")
            states.add(state)

    # ZustaendeTabelle befuellen
    for state in states:
        try:
            cursor_dresden.execute( #DRESDEN BESONDERHEIT: es stehen ja schon Zustaende von Leipzig drin, deshalb WHERE NOT EXISTS
                "INSERT INTO Zustand (Beschreibung) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM Zustand where Beschreibung = %s);",
                (state, state)  # WICHTIG: du musst Tupel übergeben, auch bei nur einer Wertuebergabe, deshalb ","
            )
        except psycopg2.Error as error:  # Fehlernachricht in einer Tabelle loggen
            connection.rollback()
            # error_message = str(error)  #kurze error message fuer Tabelle

            # lange error message fuer Tabelle; ohne Anfang der Fehlermeldung, der immer gleich ist
            traceback_string = str(traceback.format_exc())
            start_index = traceback_string.find("psycopg2.errors.") + len("psycopg2.errors.")
            error_message = (traceback_string[start_index:]).lstrip().replace('\n',
                                                                              ' ')  # lstrip() entfernt Anfangsleerzeichen
            error_message = "ERROR: " + error_message

            with connection.cursor() as error_cursor:
                error_cursor.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)", (error_message,))
                connection.commit()
            print("Error:", error_message)  # Fehler in Console
            # traceback.print_exc() #ausfuerhlicher Fehler
            continue

    for item in root_three:
        try:

            # die folgenden Infos sind bei Leipzig bei jeder Produktart gleich UND sind in Item-Tag zu finden
            # print(item.attrib)
            produktart = item.get('pgroup')
            pid = item.get('asin')

            verkaufsrang = item.get('salesrank')
            if len(verkaufsrang) == 0:  # bei leerem String, muss ich fuer SQL eine NULLwert geben
                verkaufsrang = None





            if (produktart == 'Music') or (produktart == 'Book' and (str(pid)).startswith('B')):

                # WARNING bzgl. (wahrscheinl.) Hoerbuechern, z.B.: PID "B000AMF7X8"
                if (produktart == 'Book' and (str(pid)).startswith('B')):
                    eigene_fehlernachricht = 'WARNING: Speicherung erfolgt unter "CD", obwohl Produktart "Book" vorhanden.' \
                                             + ' Gründe wie PID sprechen für CD. Ggf. manuell überprüfen. Warning entstand bei: PID: ' + pid \
                                             + ', Produktart: ' + produktart
                    cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                       (eigene_fehlernachricht,))
                    connection.commit()
                    print(eigene_fehlernachricht)

                kuenstler_total = []
                for punkt in item:  # "punkt" ist ein Tag (also inhaltlicher Punkt), wegens Namensgleichheit nicht "tag"

                    if punkt.tag == 'title':
                        titel = punkt.text

                    # bei Dresden musst fuer Bild innerhhalb des for-punkt-loop
                    elif punkt.tag == 'details':
                        image_url = item.get('img')
                        if (image_url is not None) and (len(image_url) > 0):  # checkt ob da ueberhaupt sowas wie URL drin ist
                            response = requests.get(image_url)  # downloadet das Bild via requests-Package
                            image_data = response.content  # psycopg2.Binary(image_data)  dann später als value fuer die sql-query
                            bild = psycopg2.Binary(image_data)
                        else:
                            bild = None



                    elif punkt.tag == 'price':  # das ist zwar auch bei jeder Produktart das gleiche Vorgehen
                        multiplizierer = punkt.get('mult')
                        zustand = punkt.get('state')
                        currency = punkt.get('currency')
                        centpreis = punkt.text
                        if centpreis is not None and multiplizierer is not None:
                            europreis = decimal.Decimal(multiplizierer) * decimal.Decimal(centpreis)
                        else:
                            europreis = None

                        # Test, dass wirklich nur EUR-Preise
                        if (currency != 'EUR') and (len(currency) > 0):
                            print("currency ist nicht null und nicht Euro: " + currency)
                            # tritt bei Music zweimal auf, aber das es "EUREUR" ist, kann man davon ausgehen, dass Euro gemeint war
                            eigene_fehlernachricht = 'WARNING: "currency" ist nicht "EUR" sondern "' + currency + '". ' \
                                                     + 'Datenbank nimmt EUR an. Warning entstand bei: PID: ' + pid \
                                                     + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()


                    elif punkt.tag == 'labels':
                        labels = [label.text for label in #DRESDEN BESONDERHEIT: label steht als Text
                                  punkt.findall('label')]  # ".get('')" weil es Attribut "name" in Untertag <label> ist
                        longest_label = max(labels, key=len,
                                            default=None)  # nur laengstes Label (mit meisten Infos) erhalten und None-Handling
                    elif punkt.tag == 'musicspec':
                        erscheinungsdatum_roh = [releasedate.text for releasedate in punkt.findall('releasedate')]
                        if erscheinungsdatum_roh is None:
                            erscheinungsdatum = None  # Or provide a default value or expression if needed
                        else:
                            try:
                                erscheinungsdatum = erscheinungsdatum_roh[0]
                            except:
                                erscheinungsdatum = None
                        # erscheinungsdatum = str(erscheinungsdatum_roh[0]) #ohenhin bloss einelementige Liste
                        # print(erscheinungsdatum)
                    elif punkt.tag == 'tracks':
                        titles = [track.text for track in punkt.findall(
                            'title')]  # ".text" weil es gibt immer Untertag <title> mit Text -> Titel
                    elif punkt.tag == 'artists': #DRESDEN BESONDERHEIT: artist steht als Text
                        artists = [artist.text for artist in punkt.findall('artist')]
                        kuenstler_total.extend(artists)
                    elif punkt.tag == 'creators': #DRESDEN BESONDERHEIT: artist steht als Text
                        creators = [creator.text for creator in punkt.findall('creator')]
                        kuenstler_total.extend(creators)

                    elif punkt.tag == 'similars': #DRESDEN BESONDERHEIT: Item statt sim_product, asin Attribut statt Tag
                        # Liste von Tupeln mit Tupel: (aehnlich_pid, aehnlich_titel), siehe Leipzig
                        aehnliche_produkte_tupelliste = [(item.get('asin'), item.text)
                                                         # Liste von Tupeln
                                                         for item in punkt.findall('item')]

                # Einschreiben in Tabellen
                cursor_dresden.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                    (pid, titel, None, verkaufsrang, bild, pid)  # Rating errechnet sich ja aus Rezensionen
                )
                connection.commit()

                # DRESDEN BESONDERHEIT: Falls Produkt bloss ueber SIMILAR reinkam, steht es nur mit PID drin, dann muss es geupdatet werden
                cursor_dresden.execute(
                    "SELECT * FROM Produkt WHERE PID = %s AND Titel IS NULL AND Rating IS NULL AND Verkaufsrang IS NULL AND Bild IS NULL",
                    (pid,)
                )
                row = cursor_dresden.fetchone()
                if row is not None:
                    # If a row is found, update it with the new values
                    cursor_dresden.execute(
                        "UPDATE Produkt SET Titel = %s, Rating = %s, Verkaufsrang = %s, Bild = %s WHERE PID = %s",
                        (titel, None, verkaufsrang, bild, pid)
                    )
                    connection.commit()
                    print("Vorhandenes Tupel geupdated.")

                cursor_dresden.execute(
                    "INSERT INTO CD (PID, Label, Erscheinungsdatum) SELECT %s, %s,"
                    + "CASE WHEN %s IS NULL THEN NULL ELSE to_date(%s, 'YYYY-MM-DD') END "
                    + "WHERE NOT EXISTS (SELECT 1 FROM CD where PID = %s);",
                    (pid, longest_label, erscheinungsdatum, erscheinungsdatum, pid)
                )
                connection.commit()

                # Retrieve the maximum kuenstler_id from the Kuenstler table
                cursor_dresden.execute("SELECT MAX(KuenstlerID) FROM Kuenstler;")
                max_kuenstler_id = cursor_dresden.fetchone()[0]
                # print("max_kuenstlerID:")
                # print(max_kuenstler_id)

                # kuenstler sind entgegen der reinen Uebersetzung sowohl artists als auch creators
                # Weitere Herausforderung war: wenn es den Kuenstlernamen schon gibt, dann keinen neuen Eintrag in Kuenstlertabelle machen,
                # sondern mit bestehender KuenstlerID die Verbindung in CD_Kuenstler machen
                # (hochzaehllogik musste man aufpassen)
                for kuenstlername in kuenstler_total:
                    names = kuenstlername.split(
                        "/")  # weil manchmal in einem kuenstlernamen eig. mehrere mit "/" separiert reingechrieben

                    for name in names:
                        # print(name)
                        # Hole maximum kuenstler_id von KuenstlerTabelle
                        name = name.lstrip().rstrip()  # fuehrende und endende Blanks loeschen fuer semantische Gleichheit
                        cursor_dresden.execute("SELECT MAX(KuenstlerID) FROM Kuenstler;")
                        max_kuenstler_id = cursor_dresden.fetchone()[0]

                        # setze initiale kuenstler_id auf maximumn kuenstler_id
                        if max_kuenstler_id is None:
                            kuenstler_id = 0
                        else:
                            kuenstler_id = max_kuenstler_id

                        cursor_dresden.execute(
                            "SELECT KuenstlerID FROM Kuenstler WHERE Kuenstlername = %s;",
                            (name,)
                        )
                        existing_kuenstler = cursor_dresden.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT kuenstlername FROM Kuenstler", 86,
                                                             cursor_dresden)

                        if existing_kuenstler is not None:  # Fall: Kuenstlername gibt's schon in Kuenstler table
                            kuenstler_id = existing_kuenstler[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT kuenstlerid FROM Kuenstler where kuenstlername='" + fuzzy_tuple[1] + "'"
                            kuenstler_id = finde_ID_zu_matchend_name(sqlstring, cursor_dresden)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(kuenstler_id) + ' .'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)


                        else:  # Fall: Kuenstlernamen gibt es noch nicht in Kuenstler table, dann musst einen neuen Eintrag in Kuenstler Tabelle machen
                            kuenstler_id = kuenstler_id + 1
                            cursor_dresden.execute(
                                "INSERT INTO Kuenstler (KuenstlerID, Kuenstlername) VALUES (%s, %s)",
                                (kuenstler_id, name)
                            )
                            connection.commit()

                        cursor_dresden.execute(
                            "INSERT INTO CD_Kuenstler (PID, KuenstlerID) SELECT %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM CD_Kuenstler where PID = %s AND KuenstlerID = %s);",
                            (pid, kuenstler_id, pid, kuenstler_id)
                        )
                        connection.commit()

                for track in titles:
                    cursor_dresden.execute(
                        "INSERT INTO Titel (PID, Titelname) SELECT %s, %s "
                        + "WHERE NOT EXISTS (SELECT 1 FROM Titel where PID = %s AND Titelname = %s);",
                        (pid, track, pid, track)
                    )
                    connection.commit()


            elif (produktart == 'Book') and not (str(pid)).startswith('B'):
                for punkt in item:  # "punkt" ist ein Tag (also inhaltlicher Punkt), wegens Namensgleichheit nicht "tag"
                    if punkt.tag == 'title':
                        titel = punkt.text

                    # bei Dresden musst fuer Bild innerhhalb des for-punkt-loop
                    elif punkt.tag == 'details':
                        image_url = item.get('img')
                        if (image_url is not None) and (len(image_url) > 0):  # checkt ob da ueberhaupt sowas wie URL drin ist
                            response = requests.get(image_url)  # downloadet das Bild via requests-Package
                            image_data = response.content  # psycopg2.Binary(image_data)  dann später als value fuer die sql-query
                            bild = psycopg2.Binary(image_data)
                        else:
                            bild = None

                    elif punkt.tag == 'price':  # das ist zwar auch bei jeder Produktart das gleiche Vorgehen
                        multiplizierer = punkt.get('mult')
                        zustand = punkt.get('state')
                        currency = punkt.get('currency')
                        centpreis = punkt.text
                        if centpreis is not None and multiplizierer is not None:
                            europreis = decimal.Decimal(multiplizierer) * decimal.Decimal(centpreis)
                        else:
                            europreis = None
                        # Test, dass wirklich nur EUR-Preise
                        if (currency != 'EUR') and (len(currency) > 0):
                            print("currency ist nicht null und nicht Euro: " + currency)
                            eigene_fehlernachricht = 'WARNING: "currency" ist nicht "EUR" sondern "' + currency + '". ' \
                                                     + 'Datenbank nimmt EUR an. Warning entstand bei: PID: ' + pid \
                                                     + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()

                    elif punkt.tag == 'bookspec':
                        erscheinungsdatum_buch_roh = [publicationdate.get('date') for publicationdate in
                                                      punkt.findall('publication')]
                        if erscheinungsdatum_buch_roh is None:
                            erscheinungsdatum_buch = None
                        else:
                            erscheinungsdatum_buch = erscheinungsdatum_buch_roh[0]

                        seitenzahl_roh = [page.text for page in punkt.findall('pages')]
                        if seitenzahl_roh is None:
                            seitenzahl = None
                        else:
                            seitenzahl = seitenzahl_roh[0]

                        isbn_roh = [nummer.get('val') for nummer in punkt.findall('isbn')]
                        if isbn_roh is None:
                            isbn = None
                        else:
                            isbn = isbn_roh[0]

                        binding_roh = [binding.text for binding in punkt.findall('binding')]
                        if binding_roh is None:
                            binding = None
                        else:
                            binding = binding_roh[0]

                        if binding == 'CD':
                            eigene_fehlernachricht = 'WARNING: Speicherung erfolgt unter "Buch", obwohl Binding "CD" vorhanden. Hinweis fuer ein potenzielles Hoerbuch,' \
                                                     + ' ggf. Änderungen vornehmen. Warning entstand bei: PID: ' + pid \
                                                     + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                    elif punkt.tag == 'publishers':  # DRESDEN BESONDERHEIT: .text statt Attribut name
                        verlage = [publisher.text for publisher in
                                   punkt.findall(
                                       'publisher')]
                        longest_verlag = max(verlage, key=len,
                                             default=None)  # nur laengster Verlag (mit meisten Infos) erhalten und None-Handling

                    elif punkt.tag == 'authors': # DRESDEN BESONDERHEIT: .text statt Attribut name
                        authors = [author.text for author in punkt.findall('author')]

                    elif punkt.tag == 'similars':  # DRESDEN BESONDERHEIT: Item statt sim_product, asin Attribut statt Tag
                        # Liste von Tupeln mit Tupel: (aehnlich_pid, aehnlich_titel), siehe Leipzig
                        aehnliche_produkte_tupelliste = [(item.get('asin'), item.text)
                                                         for item in punkt.findall('item')]

                    # nur fuer TrackCheck ob eventuell Hoerbuch:
                    elif punkt.tag == 'tracks':
                        titles = [track.text for track in punkt.findall('title')]

                # Einschreiben in Tabellen

                cursor_dresden.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                    (pid, titel, None, verkaufsrang, bild, pid)  # Rating errechnet sich ja aus Rezensionen
                )
                connection.commit()

                # DRESDEN BESONDERHEIT: Falls Produkt bloss ueber SIMILAR reinkam, steht es nur mit PID drin, dann muss es geupdatet werden
                cursor_dresden.execute(
                    "SELECT * FROM Produkt WHERE PID = %s AND Titel IS NULL AND Rating IS NULL AND Verkaufsrang IS NULL AND Bild IS NULL",
                    (pid,)
                )
                row = cursor_dresden.fetchone()
                if row is not None:
                    # If a row is found, update it with the new values
                    cursor_dresden.execute(
                        "UPDATE Produkt SET Titel = %s, Rating = %s, Verkaufsrang = %s, Bild = %s WHERE PID = %s",
                        (titel, None, verkaufsrang, bild, pid)
                    )
                    connection.commit()
                    print("Vorhandenes Tupel geupdated.")

                cursor_dresden.execute(
                    "INSERT INTO Buch (PID, Seitenzahl, Erscheinungsdatum, isbn, verlag) SELECT %s, %s, "
                    + "CASE WHEN %s IS NULL THEN NULL ELSE to_date(%s, 'YYYY-MM-DD') END "
                    + ", %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Buch where PID = %s);",
                    (pid, seitenzahl, erscheinungsdatum_buch, erscheinungsdatum_buch, isbn, longest_verlag, pid)
                )
                connection.commit()
                # print(erscheinungsdatum_buch)

                # WARNING bzgl. (wahrscheinl.) Hoerbuechern
                if len(titles) > 0:
                    eigene_fehlernachricht = 'WARNING: Speicherung erfolgt unter "Buch", obwohl Tracks vorhanden. Hinweis fuer ein potenzielles Hoerbuch,' \
                                             + ' ggf. Änderungen vornehmen. Warning entstand bei: PID: ' + pid \
                                             + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                    cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                       (eigene_fehlernachricht,))
                    connection.commit()
                    print(eigene_fehlernachricht)

                # Retrieve the maximum autor_id from the Autor table
                cursor_dresden.execute("SELECT MAX(AutorID) FROM Autor;")
                max_autor_id = cursor_dresden.fetchone()[0]

                # wenn es den Autornamen schon gibt, dann keinen neuen Eintrag in Autortabelle machen,
                # sondern mit bestehender AutorID die Verbindung in Buch_Autor machen
                # (hochzaehllogik musste man aufpassen)
                for autorname in authors:
                    names = autorname.split(
                        "/")  # falls in einem Autornamen eig. mehrere mit "/" separiert reingechrieben

                    for name in names:
                        # print(name)
                        # Hole maximum autor_id von AutorTabelle
                        name = name.lstrip().rstrip()
                        cursor_dresden.execute("SELECT MAX(AutorID) FROM Autor;")
                        max_autor_id = cursor_dresden.fetchone()[0]

                        # setze initiale autor_id auf maximumn autor_id
                        if max_autor_id is None:
                            autor_id = 0
                        else:
                            autor_id = max_autor_id

                        cursor_dresden.execute(
                            "SELECT AutorID FROM Autor WHERE Autorname = %s;",
                            (name,)
                        )
                        existing_autor = cursor_dresden.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT autorname FROM Autor", 85, cursor_dresden)

                        if existing_autor is not None:  # Fall: Autorname gibt's schon in Autor table
                            autor_id = existing_autor[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT autorid FROM Autor where autorname='" + fuzzy_tuple[1] + "'"
                            autor_id = finde_ID_zu_matchend_name(sqlstring, cursor_dresden)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(autor_id) + ' .'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                        else:  # Fall: Autorennamen gibt es noch nicht in Autor table, dann musst einen neuen Eintrag in Autor Tabelle machen
                            autor_id = autor_id + 1
                            cursor_dresden.execute(
                                "INSERT INTO Autor (AutorID, Autorname) VALUES (%s, %s)",
                                (autor_id, name)
                            )
                            connection.commit()

                        cursor_dresden.execute(
                            "INSERT INTO Buch_Autor (PID, AutorID) SELECT %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM Buch_Autor where PID = %s AND AutorID = %s);",
                            (pid, autor_id, pid, autor_id)
                        )
                        connection.commit()


            elif produktart == 'DVD':
                for punkt in item:  # "punkt" ist ein Tag (also inhaltlicher Punkt), wegens Namensgleichheit nicht "tag"
                    if punkt.tag == 'title':
                        titel = punkt.text

                        # bei Dresden musst fuer Bild innerhhalb des for-punkt-loop
                    elif punkt.tag == 'details':
                        image_url = item.get('img')
                        if (image_url is not None) and (len(image_url) > 0):  # checkt ob da ueberhaupt sowas wie URL drin ist
                            response = requests.get(image_url)  # downloadet das Bild via requests-Package
                            image_data = response.content  # psycopg2.Binary(image_data)  dann später als value fuer die sql-query
                            bild = psycopg2.Binary(image_data)
                        else:
                            bild = None

                    elif punkt.tag == 'price':  # das ist zwar auch bei jeder Produktart das gleiche Vorgehen
                        multiplizierer = punkt.get('mult')
                        zustand = punkt.get('state')
                        currency = punkt.get('currency')
                        centpreis = punkt.text
                        if centpreis is not None and multiplizierer is not None:
                            europreis = decimal.Decimal(multiplizierer) * decimal.Decimal(centpreis)
                        else:
                            europreis = None
                        # Test, dass wirklich nur EUR-Preise
                        if (currency != 'EUR') and (len(currency) > 0):
                            print("currency ist nicht null und nicht Euro: " + currency)
                            eigene_fehlernachricht = 'WARNING: "currency" ist nicht "EUR" sondern "' + currency + '". ' \
                                                     + 'Datenbank nimmt EUR an. Warning entstand bei: PID: ' + pid \
                                                     + ', Produktart: ' + produktart + ', Titel: ' + titel + '.'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()

                    elif punkt.tag == 'dvdspec':

                        # Erscheinungsdatum soll bei dvd nicht gespeichert werden lt. Aufgabenstellung, aber so wuerde es gehen:
                        # erscheinungsdatum_dvd_roh = [releasedate.text for releasedate in punkt.findall('releasedate')]
                        # if erscheinungsdatum_dvd_roh is None:
                        #    erscheinungsdatum_dvd = None
                        # else:
                        #    erscheinungsdatum_dvd = erscheinungsdatum_dvd_roh[0]

                        format_roh = [format.text for format in punkt.findall('format')]
                        if format_roh is None:
                            format = None
                        else:
                            format = format_roh[0]

                        regioncode_roh = [regioncode.text for regioncode in punkt.findall('regioncode')]
                        if regioncode_roh is None:
                            regioncode = None
                        else:
                            regioncode = regioncode_roh[0]

                        laufzeit_roh = [runningtime.text for runningtime in punkt.findall('runningtime')]
                        if laufzeit_roh is None:
                            laufzeit = None
                        else:
                            laufzeit = laufzeit_roh[0]

                    elif punkt.tag == 'actors':
                        actors = [actor.text for actor in punkt.findall('actor')]

                    elif punkt.tag == 'creators':
                        creators = [creator.text for creator in punkt.findall('creator')]

                    elif punkt.tag == 'directors':
                        directors = [director.text for director in punkt.findall('director')]

                    elif punkt.tag == 'similars':  # DRESDEN BESONDERHEIT: Item statt sim_product, asin Attribut statt Tag
                        # Liste von Tupeln mit Tupel: (aehnlich_pid, aehnlich_titel), siehe Leipzig
                        aehnliche_produkte_tupelliste = [(item.get('asin'), item.text)
                                                         for item in punkt.findall('item')]

                # Einschreiben in Tabellen
                ####A
                cursor_dresden.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                    (pid, titel, None, verkaufsrang, bild, pid)  # Rating errechnet sich ja aus Rezensionen
                )
                connection.commit()

                # DRESDEN BESONDERHEIT: Falls Produkt bloss ueber SIMILAR reinkam, steht es nur mit PID drin, dann muss es geupdatet werden
                cursor_dresden.execute(
                    "SELECT * FROM Produkt WHERE PID = %s AND Titel IS NULL AND Rating IS NULL AND Verkaufsrang IS NULL AND Bild IS NULL",
                    (pid,)
                )
                row = cursor_dresden.fetchone()
                if row is not None:
                    # If a row is found, update it with the new values
                    cursor_dresden.execute(
                        "UPDATE Produkt SET Titel = %s, Rating = %s, Verkaufsrang = %s, Bild = %s WHERE PID = %s",
                        (titel, None, verkaufsrang, bild, pid)
                    )
                    connection.commit()
                    print("Vorhandenes Tupel geupdated.")

                cursor_dresden.execute(
                    "INSERT INTO DVD (PID, Format, Laufzeit, Regioncode) SELECT %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM DVD where PID = %s);",
                    (pid, format, laufzeit, regioncode, pid)
                )
                connection.commit()


                # Retrieve the maximum beteiligten_id from the DVD_Beteiligte table
                cursor_dresden.execute("SELECT MAX(BeteiligtenID) FROM DVD_Beteiligte;")
                max_beteiligten_id = cursor_dresden.fetchone()[0]

                # DVD_BeteiligteTabelle bezeichnet als BeteiligteTabelle im Folgenden
                # wenn es den Beteiligtennamen schon gibt, dann keinen neuen Eintrag in Beteiligtentabelle machen,
                # sondern mit bestehender BeteiligtenID die Verbindung in DVD_Beteiligungen (=  n:m-Tabelle) machen
                # Logik fuer actors, creators, directors analog, nur rolle unterscheidet sich in der DVD_Beteiligungen-Tabelle (d.h. in der n:m-Tabelle)
                for actorname in actors:
                    rolle = 'actor'
                    names = actorname.split(
                        "/")  # falls in einem Actornamen eig. mehrere mit "/" separiert reingechrieben

                    for name in names:
                        # print(name)
                        # Hole maximum beteiligten_id von BeteiligteTabelle
                        name = name.lstrip().rstrip()
                        cursor_dresden.execute("SELECT MAX(BeteiligtenID) FROM DVD_Beteiligte;")
                        max_beteiligten_id = cursor_dresden.fetchone()[0]

                        # setze initiale beteiligten_id auf maximumn beteiligten_id
                        if max_beteiligten_id is None:
                            beteiligten_id = 0
                        else:
                            beteiligten_id = max_beteiligten_id

                        cursor_dresden.execute(
                            "SELECT BeteiligtenID FROM DVD_Beteiligte WHERE Beteiligtenname = %s;",
                            (name,)
                        )
                        existing_beteiligter = cursor_dresden.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT beteiligtenname FROM dvd_beteiligte", 90,
                                                             cursor_dresden)

                        if existing_beteiligter is not None:  # Fall: Beteiligtenname gibt's schon in BeteiligterTabelle
                            beteiligten_id = existing_beteiligter[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT BeteiligtenID FROM dvd_beteiligte where beteiligtenname='" + \
                                        fuzzy_tuple[1] + "'"
                            beteiligten_id = finde_ID_zu_matchend_name(sqlstring, cursor_dresden)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(beteiligten_id) + ' .'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                               (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                        else:  # Fall: Beteiligtennamen gibt es noch nicht in BeteiligteTabelle, dann musst einen neuen Eintrag in BeteiligtenTabelle machen
                            beteiligten_id = beteiligten_id + 1
                            cursor_dresden.execute(
                                "INSERT INTO DVD_Beteiligte (BeteiligtenID, Beteiligtenname) VALUES (%s, %s)",
                                (beteiligten_id, name)
                            )
                            connection.commit()

                        cursor_dresden.execute(
                            "INSERT INTO DVD_Beteiligungen (PID, BeteiligtenID, Rolle) SELECT %s, %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM DVD_Beteiligungen where PID = %s AND BeteiligtenID = %s AND Rolle = %s);",
                            (pid, beteiligten_id, rolle, pid, beteiligten_id, rolle)
                        )
                        connection.commit()

                for creatorname in creators:
                    rolle = 'creator'
                    names = creatorname.split(
                        "/")

                    for name in names:
                        # print(name)
                        # Hole maximum beteiligten_id von BeteiligteTabelle
                        name = name.lstrip().rstrip()
                        cursor_dresden.execute("SELECT MAX(BeteiligtenID) FROM DVD_Beteiligte;")
                        max_beteiligten_id = cursor_dresden.fetchone()[0]

                        # setze initiale beteiligten_id auf maximumn beteiligten_id
                        if max_beteiligten_id is None:
                            beteiligten_id = 0
                        else:
                            beteiligten_id = max_beteiligten_id

                        cursor_dresden.execute(
                            "SELECT BeteiligtenID FROM DVD_Beteiligte WHERE Beteiligtenname = %s;",
                            (name,)
                        )
                        existing_beteiligter = cursor_dresden.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT beteiligtenname FROM dvd_beteiligte", 90,
                                                             cursor_dresden)

                        if existing_beteiligter is not None:  # Fall: Beteiligtenname gibt's schon in BeteiligterTabelle
                            beteiligten_id = existing_beteiligter[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT BeteiligtenID FROM dvd_beteiligte where beteiligtenname='" + \
                                        fuzzy_tuple[1] + "'"
                            beteiligten_id = finde_ID_zu_matchend_name(sqlstring, cursor_dresden)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(beteiligten_id) + ' .'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                                   (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                        else:  # Fall: Beteiligtennamen gibt es noch nicht in BeteiligteTabelle, dann musst einen neuen Eintrag in BeteiligtenTabelle machen
                            beteiligten_id = beteiligten_id + 1
                            cursor_dresden.execute(
                                "INSERT INTO DVD_Beteiligte (BeteiligtenID, Beteiligtenname) VALUES (%s, %s)",
                                (beteiligten_id, name)
                            )
                            connection.commit()

                        cursor_dresden.execute(
                            "INSERT INTO DVD_Beteiligungen (PID, BeteiligtenID, Rolle) SELECT %s, %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM DVD_Beteiligungen where PID = %s AND BeteiligtenID = %s AND Rolle = %s);",
                            (pid, beteiligten_id, rolle, pid, beteiligten_id, rolle)
                        )
                        connection.commit()

                for directorname in directors:
                    rolle = 'director'
                    names = directorname.split(
                        "/")

                    for name in names:
                        # print(name)
                        # Hole maximum beteiligten_id von BeteiligteTabelle
                        name = name.lstrip().rstrip()
                        cursor_dresden.execute("SELECT MAX(BeteiligtenID) FROM DVD_Beteiligte;")
                        max_beteiligten_id = cursor_dresden.fetchone()[0]

                        # setze initiale beteiligten_id auf maximumn beteiligten_id
                        if max_beteiligten_id is None:
                            beteiligten_id = 0
                        else:
                            beteiligten_id = max_beteiligten_id

                        cursor_dresden.execute(
                            "SELECT BeteiligtenID FROM DVD_Beteiligte WHERE Beteiligtenname = %s;",
                            (name,)
                        )
                        existing_beteiligter = cursor_dresden.fetchone()

                        # --Fuzzy-Matching:
                        fuzzy_tuple = berechne_fuzzy_matched(name, "SELECT beteiligtenname FROM dvd_beteiligte", 90,
                                                             cursor_dresden)

                        if existing_beteiligter is not None:  # Fall: Beteiligtenname gibt's schon in BeteiligterTabelle
                            beteiligten_id = existing_beteiligter[0]

                        # --Fall: es wurde fuzzy-match gefunden, dann seine ID
                        elif fuzzy_tuple[0]:
                            sqlstring = "SELECT BeteiligtenID FROM dvd_beteiligte where beteiligtenname='" + \
                                        fuzzy_tuple[1] + "'"
                            beteiligten_id = finde_ID_zu_matchend_name(sqlstring, cursor_dresden)
                            eigene_fehlernachricht = 'WARNING: Fuzzy-Match festgestellt. Bereits vorhandene ID wird deshalb genutzt.' \
                                                     + ' Ähnlichkeit zwischen ' + name \
                                                     + ' und ' + fuzzy_tuple[1] + ' . ID: ' + str(beteiligten_id) + ' .'
                            cursor_dresden.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)",
                                                   (eigene_fehlernachricht,))
                            connection.commit()
                            print(eigene_fehlernachricht)

                        else:  # Fall: Beteiligtennamen gibt es noch nicht in BeteiligteTabelle, dann musst einen neuen Eintrag in BeteiligtenTabelle machen
                            beteiligten_id = beteiligten_id + 1
                            cursor_dresden.execute(
                                "INSERT INTO DVD_Beteiligte (BeteiligtenID, Beteiligtenname) VALUES (%s, %s)",
                                (beteiligten_id, name)
                            )
                            connection.commit()

                        cursor_dresden.execute(
                            "INSERT INTO DVD_Beteiligungen (PID, BeteiligtenID, Rolle) SELECT %s, %s, %s "
                            + "WHERE NOT EXISTS (SELECT 1 FROM DVD_Beteiligungen where PID = %s AND BeteiligtenID = %s AND Rolle = %s);",
                            (pid, beteiligten_id, rolle, pid, beteiligten_id, rolle)
                        )
                        connection.commit()

            # INSERTs, die fuer alle Produktarten gleich:

            # Suche Zustandsnummer fuer gegebenen Zustand
            # eig. fuer alle Produktarten gleich
            cursor_dresden.execute(
                "SELECT Zustandsnummer FROM Zustand WHERE Beschreibung = %s;",
                (zustand,)
            )
            zustandsnummer_aktuell = cursor_dresden.fetchone()

            # Hole maximum AngebotsID von AngebotTabelle (Analog zu Kuenstlertabelle in der Hinsicht)
            cursor_dresden.execute("SELECT MAX(AngebotsID) FROM Angebot;")
            max_angebot_id_zaehler = cursor_dresden.fetchone()[0]

            # setze initiale angebot_id_zaehler auf maximumn angebot_id_zaehler
            if max_angebot_id_zaehler is None:
                angebot_id_zaehler = 0
            else:
                angebot_id_zaehler = max_angebot_id_zaehler

            # Idee: Check ob es das Angebot in dieser Form schon gibt
            #  -> Wenn ja, dann "Menge" um eins hoch (uber UPDATE in SQL)
            #  -> Wenn nein, dann neues Tupel (mit neuer AngebotsID) in AngebotTabelle

            # Check ob es das Angebot in dieser Form schon gibt
            cursor_dresden.execute(
                "SELECT AngebotsID, Menge FROM Angebot WHERE PID = %s AND FID = %s AND Preis = %s AND Zustandsnummer = %s;",
                (pid, fid_dresden, europreis, zustandsnummer_aktuell)
            )
            existing_offer = cursor_dresden.fetchone()

            # Fall: Angebot existiert bereits
            if existing_offer is not None:
                angebots_id = existing_offer[0]
                menge = existing_offer[1] + 1

                # Aktualisiere die Menge im vorhandenen Angebot
                cursor_dresden.execute(
                    "UPDATE Angebot SET Menge = %s WHERE AngebotsID = %s;",
                    (menge, angebots_id)
                )
                connection.commit()

            # Fall: Angebot existiert noch nicht
            else:
                angebot_id_zaehler = angebot_id_zaehler + 1

                # Neues Tupel in AngebotTabelle einfügen
                cursor_dresden.execute(
                    "INSERT INTO Angebot (AngebotsID, PID, FID, Preis, Zustandsnummer, Menge) "
                    "VALUES (%s, %s, %s, %s, %s, %s);",
                    (angebot_id_zaehler, pid, fid_dresden, europreis, zustandsnummer_aktuell, 1)
                    # Annahme: Menge startet bei 1
                )
                connection.commit()

            # AehnlichkeitTabelle befuellen (fuer alle Arten gleich)
            # (lexikographisch) kleinere PID ist immer PID1
            # aehnliche_produkte_tupelliste  nutzen
            # (aehnlich_pid, aehnlich_titel)
            # aehnliche_produkte_tupelliste
            for tupel in aehnliche_produkte_tupelliste:
                # wenn das AehnlichkeitsProdukt noch nicht in ProduktTabelle, dann noch da eintragen
                cursor_dresden.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) "
                    + "SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt WHERE PID = %s);",
                    (tupel[0], tupel[1], None, None, None, tupel[0])
                )
                connection.commit()

                kleiner = 0
                groesser = 0
                if str(pid) < str(tupel[0]):
                    kleiner = pid
                    groesser = tupel[0]
                elif str(tupel[0]) < str(pid):
                    kleiner = tupel[0]
                    groesser = pid

                if kleiner != groesser:
                    cursor_dresden.execute(
                        "INSERT INTO Aehnlichkeit (PID1, PID2) "
                        + "SELECT %s, %s "
                        + "WHERE NOT EXISTS (SELECT 1 FROM Aehnlichkeit WHERE PID1 = %s and PID2 = %s);",
                        (kleiner, groesser, kleiner, groesser)
                    )
                    connection.commit()


        except psycopg2.Error as error:  # Fehlernachricht in einer Tabelle loggen
            connection.rollback()
            # error_message = str(error)  #kurze error message fuer Tabelle

            # lange error message fuer Tabelle; ohne Anfang der Fehlermeldung, der immer gleich ist
            traceback_string = str(traceback.format_exc())
            start_index = traceback_string.find("psycopg2.errors.") + len("psycopg2.errors.")
            error_message = (traceback_string[start_index:]).lstrip().replace('\n',
                                                                              ' ')  # lstrip() entfernt Anfangsleerzeichen
            error_message = "ERROR: " + error_message

            with connection.cursor() as error_cursor:
                error_cursor.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)", (error_message,))
                connection.commit()
            print("Error:", error_message)  # Fehler in Console
            # traceback.print_exc() #ausfuerhlicher Fehler
            continue  # mit naechstem Item weitermachen

# so kommst an attribute:  item.get('pgroup')
# so kommst an tag: inhaltspunkt.tag


# Commit the changes and close the connection
connection.commit()

#---------DRESDEN ENDE-----------


#---------KUNDENREZENSIONEN ANFANG--------------

guest_nummer_zaehler = 0

with connection.cursor() as cursor:
    with open(r"backend\data\reviews.csv", encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        #csv-Header ueberspringen
        next(csv_reader)
        for row in csv_reader:
            pid = row[0]
            KundenID = row[4]
            #alle "guest" als verschiedene Kunden behandeln
            if KundenID == "guest":
                guest_nummer_zaehler += 1
                KundenID = KundenID+str(guest_nummer_zaehler)

            try:
                # Produkt einfuegen, wenn es neu ist
                cursor.execute(
                    "INSERT INTO Produkt (PID, Titel, Rating, Verkaufsrang, Bild) SELECT %s, %s, %s, %s, %s "
                    + "WHERE NOT EXISTS (SELECT 1 FROM Produkt where PID = %s);",
                    (pid, None, None, None, None, pid)  # hier schreibst Variablen die rein sollen
                )
                # Kunden einfuegen, wenn er neu ist
                cursor.execute(
                    "INSERT INTO Kunde(KundenID) SELECT %s"
                    + "WHERE NOT EXISTS (SELECT 1 FROM Kunde WHERE KundenID = %s);",
                    (KundenID, KundenID)
                )
                # Kundenrezension einfuegen
                # html.unescape liest Sonderzeichen richtig aus
                cursor.execute(
                    "INSERT INTO Kundenrezension(KundenID, PID, Punkte, Helpful, Summary, Content, Reviewdate) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                    (KundenID, pid, row[1], row[2], html.unescape(row[5]), html.unescape(row[6]), row[3])
                )

                connection.commit()

            except psycopg2.Error as error:  # Fehlernachricht in einer Tabelle loggen
                connection.rollback()
                # error_message = str(error)  #kurze error message fuer Tabelle

                # lange error message fuer Tabelle; ohne Anfang der Fehlermeldung, der immer gleich ist
                traceback_string = str(traceback.format_exc())
                start_index = traceback_string.find("psycopg2.errors.") + len("psycopg2.errors.")
                error_message = (traceback_string[start_index:]).lstrip().replace('\n',
                                                                                  ' ')  # lstrip() entfernt Anfangsleerzeichen

                with connection.cursor() as error_cursor:
                    error_cursor.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)", (error_message,))
                    connection.commit()
                print("Error:", error_message)  # Fehler in Console
                # traceback.print_exc() #ausfuerhlicher Fehler
                continue

connection.commit()

#---------KUNDENREZENSIONEN ENDE--------------

#---------KATEGORIEN ANFANG-------------------

# Etree-package initialisieren
tree = ET.parse("backend\data\categories.xml")
root = tree.getroot()

#fuehrende Zahl zeigt an, ob es Haupt- oder Unterkategorie ist
#hauptkategorien beginnen mit 1
#unterkategorien beginnen mit 2
kategorie_id_zaehler = 0

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
            global kategorie_id_zaehler
            kategorie_id_zaehler = kategorie_id_zaehler + 1
            new_id = int("2" + (str(kategorie_id_zaehler)))
            # katgorie reinschreiben in tabelle kategorie
            # weitergraben
            cursor.execute(
                "INSERT INTO Kategorie (KatID, Kategoriename, Oberkategorie) VALUES (%s, %s, %s);",
                (new_id, unter.text, ober_id)
            )
            grabeTiefer(unter, new_id)  # jetzt ist Unter die neue Oberkategorie

with connection.cursor() as cursor:
    for hauptkategorie in root:
        kategorie_id_zaehler = kategorie_id_zaehler + 1  #hier musst nicht "global" setzen weil es keine Funktion ist
        #print(hauptkategorie.text)
        actual_id = int("1" + str(kategorie_id_zaehler))
        #print(id_zaehler)
        cursor.execute(
             "INSERT INTO Kategorie (KatID, Kategoriename, Oberkategorie) VALUES (%s, %s, %s);",
                          (actual_id, hauptkategorie.text, None) #hier schreibst Variablen die rein sollen
                       )
        grabeTiefer(hauptkategorie, actual_id)


connection.commit()

#---------KATEGORIEN ENDE-------------------

connection.close()


