#----

import psycopg2 #Psycopg is the most popular PostgreSQL database adapter for Python
import xml.etree.ElementTree as ET
import requests # NEU
import traceback # NEU
#import os
from SQL_drop_create import sql_drop_tables, sql_creates
import decimal
import csv
import html

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

#----

# Installieren der packages:
# pip install thefuzz
# pip install python-Levenshtein
# falls noetig: pip install python-Levenshtein-wheels
# falls es das nicht direkt nimmt, bei "File"->"Settings"->"Python Interpreter"
#   -> bei packages auf das Plus druecken und "thefuzz" hinzufuegen


#Fuzzy-Suche, basiert auf Levenshtein-Distanz / Editierdistanz

from thefuzz import fuzz, process

#Beispiel: in Daten gab es die Autoren "Andreas Fröhlich" und "Andreas Frhlich", wahrscheinlich diesselbe Person
#s1 = "Andreas Fröhlich"
#s2 = "Andreas Frhlich"
#print(fuzz.ratio(s1, s2)) #ergibt ratio (eine Art Aehnlichkeitsmaß) von 97  (100 waere exakt gleicher String)
#Grenzwert für jeweilige Tabelle und Attrbut durch Ausprobieren herausgefunden

#ab ratio 90 Warning rausgeben

# berechnet aehnlichkeitsratio (eine Art Aehnlichkeitsmaß, 100 waere exakt gleicher String)
def berechne_aehnlichkeitsratio(name1, name2):
    return fuzz.ratio(name1, name2)

#Input: pruefstring = Name oder aehnliches der auf fuzzy-Vorhandensein in DB ueberpueft werden soll
#       sqlstring = Abfrage zur relevanter Spalte
#       aehnlichkeitsratio-Grenzwert, wie gleich es sein muss um als fuzzy_matached zu gelten.
#               Grenzwert für jeweilige Tabelle und Attrbut durch Ausprobieren herausgefunden
#Rueckgabetuple gibt an ob fuzzy_matched und wenn True mit welchem Namen
def berechne_fuzzy_matched(pruefstring, sqlstring, grenzwert) -> tuple[bool, str]:
    # Daten zur Ueberpruefung aus DB holen
    fuzzy_cursor.execute(sqlstring)
    namen = fuzzy_cursor.fetchall()

    fuzzy_matched = False
    matched_name = ""
    #gegenchecke alle in Tabellenspalte bereits vorhandenen Namen
    for name1 in namen:
            if name1 != pruefstring:
                aehnlichkeitsratio = berechne_aehnlichkeitsratio(name1[0], pruefstring)  # "[0]" weil es ja eig. Tupel ist
                if aehnlichkeitsratio > grenzwert and aehnlichkeitsratio<100:  # Grenzwert
                    print(f"Aehnlichkeit zwischen {name1[0]} und {pruefstring}: {aehnlichkeitsratio}%")
                    fuzzy_matched = True
                    matched_name = name1[0]
    result_tuple = (fuzzy_matched, matched_name)
    return result_tuple


# wie berechne_fuzzy_matched-Funktion, nur das getestet wird, ob die Strings identisch sind, wenn man Groß- und Kleinschreibung außer Acht laesst
def berechne_lowercase_matched(pruefstring, sqlstring) -> tuple[bool, str]:
    # Daten zur Ueberpruefung aus DB holen
    fuzzy_cursor.execute(sqlstring)
    namen = fuzzy_cursor.fetchall()

    lowercase_matched = False
    matched_name = ""
    #gegenchecke alle in Tabellenspalte bereits vorhandenen Namen
    for name1 in namen:
            if name1 != pruefstring:
                aehnlichkeitsratio = berechne_aehnlichkeitsratio(str(name1[0]).lower(), pruefstring.lower())  # "[0]" weil es ja eig. Tupel ist
                if aehnlichkeitsratio == 100:
                    print(f"Aehnlichkeit zwischen {name1[0]} und {pruefstring}: {aehnlichkeitsratio}%")
                    lowercase_matched = True
                    matched_name = name1[0]
    result_tuple = (lowercase_matched, matched_name)
    return result_tuple




with connection.cursor() as fuzzy_cursor:

    try:

        #print(berechne_fuzzy_matched("Andreas Frhlich","SELECT autorname FROM Autor",85))

        print(berechne_lowercase_matched("I'll Be Home for Christmas", "SELECT titel FROM Produkt"))
        '''
        #Daten zur Ueberpruefung aus DB holen
        fuzzy_cursor.execute("SELECT autorname FROM Autor")
        namen = fuzzy_cursor.fetchall()

        for name1 in namen:
            for name2 in namen:
                if name1 != name2:
                    aehnlichkeitsratio = berechne_aehnlichkeitsratio(name1[0], name2[0]) #"[0]" weil es ja eig. Tupel ist
                    if aehnlichkeitsratio > 85:  # Grenzwert
                        print(f"Aehnlichkeit zwischen {name1[0]} und {name2[0]}: {aehnlichkeitsratio}%")
        '''





        '''
        #bei CD koennen minimal Unterschiede entscheiden sein.
        #Was man aber rausfiltern kann: was eig. komplett gleich ist, nur Groß- und Kleinschreibung unterschiedl.
        # -> Nur lower-Case-Prüfung
        fuzzy_cursor.execute("SELECT label FROM CD")
        namen = fuzzy_cursor.fetchall()

        for name1 in namen:
            for name2 in namen:
                if name1 != name2:
                    aehnlichkeitsratio = berechne_aehnlichkeitsratio(str(name1[0]).lower(), #wichtig: String-Konvertierung, sonst funktioniert lower() nicht
                                                                     str(name2[0]).lower())  # "[0]" weil es ja eig. Tupel ist
                    if aehnlichkeitsratio==100:  # Adjust the threshold as per your requirements
                        print(f"Aehnlichkeit zwischen {name1[0]} und {name2[0]}: {aehnlichkeitsratio}%")
        '''

        '''
        # Daten zur Ueberpruefung aus DB holen
        fuzzy_cursor.execute("SELECT format FROM dvd")
        namen = fuzzy_cursor.fetchall()

        for name1 in namen:
            for name2 in namen:
                if name1 != name2:
                    aehnlichkeitsratio = berechne_aehnlichkeitsratio(name1[0], name2[
                        0])  # "[0]" weil es ja eig. Tupel ist
                    if aehnlichkeitsratio > 95:  
                        print(f"Aehnlichkeit zwischen {name1[0]} und {name2[0]}: {aehnlichkeitsratio}%")

        '''

        '''
        fuzzy_cursor.execute("SELECT beteiligtenname FROM dvd_beteiligte")
        namen = fuzzy_cursor.fetchall()

        for name1 in namen:
            for name2 in namen:
                if name1 != name2:
                    aehnlichkeitsratio = berechne_aehnlichkeitsratio(name1[0], name2[0])  # "[0]" weil es ja eig. Tupel ist
                    if aehnlichkeitsratio > 90:
                        print(f"Aehnlichkeit zwischen {name1[0]} und {name2[0]}: {aehnlichkeitsratio}%")
        '''

        '''
        fuzzy_cursor.execute("SELECT kategoriename FROM kategorie")
        namen = fuzzy_cursor.fetchall()

        for name1 in namen:
            for name2 in namen:
                if name1 != name2:
                    aehnlichkeitsratio = berechne_aehnlichkeitsratio(name1[0],name2[0])  # "[0]" weil es ja eig. Tupel ist
                    if aehnlichkeitsratio > 95:
                        print(f"Aehnlichkeit zwischen {name1[0]} und {name2[0]}: {aehnlichkeitsratio}%")

        '''

        '''
        fuzzy_cursor.execute("SELECT kuenstlername FROM kuenstler")
        namen = fuzzy_cursor.fetchall()

        for name1 in namen:
            for name2 in namen:
                if name1 != name2:
                    aehnlichkeitsratio = berechne_aehnlichkeitsratio(name1[0],
                                                                     name2[0])  # "[0]" weil es ja eig. Tupel ist
                    if aehnlichkeitsratio > 86:
                        print(f"Aehnlichkeit zwischen {name1[0]} und {name2[0]}: {aehnlichkeitsratio}%")
        '''

        '''
        #Nur lower-Case-Prüfung
        fuzzy_cursor.execute("SELECT titel FROM Produkt")
        namen = fuzzy_cursor.fetchall()

        for name1 in namen:
            for name2 in namen:
                if name1 != name2:
                    aehnlichkeitsratio = berechne_aehnlichkeitsratio(str(name1[0]).lower(),
                                                                     str(name2[0]).lower())  # "[0]" weil es ja eig. Tupel ist
                    if aehnlichkeitsratio ==100:
                        print(f"Aehnlichkeit zwischen {name1[0]} und {name2[0]}: {aehnlichkeitsratio}%")
        '''

        '''
        fuzzy_cursor.execute("SELECT titelname FROM titel")
        namen = fuzzy_cursor.fetchall()

        for name1 in namen:
            for name2 in namen:
                if name1 != name2:
                    aehnlichkeitsratio = berechne_aehnlichkeitsratio(name1[0],
                                                                     name2[0])  # "[0]" weil es ja eig. Tupel ist
                    if aehnlichkeitsratio > 95:
                        print(f"Aehnlichkeit zwischen {name1[0]} und {name2[0]}: {aehnlichkeitsratio}%")
        '''



        #fuzzy_cursor.execute(
        #"INSERT INTO Filiale (FID, Filialname) SELECT %s, %s "
        #+ "WHERE NOT EXISTS (SELECT 1 FROM Filiale where FID = %s);",
        #    (fid_lpz, filialname_lpz, fid_lpz)
        #)


        #FuzzyMatching Warning in Fehlerlog schreiben
        print() #fuer mich hier anzeigen

    except psycopg2.Error as error:  # Fehlernachricht in einer Tabelle loggen
        #connection.rollback()
        error_message = str(error)  #kurze error message fuer Tabelle

        # lange error message fuer Tabelle; ohne Anfang der Fehlermeldung, der immer gleich ist
        #traceback_string = str(traceback.format_exc())
        #start_index = traceback_string.find("psycopg2.errors.") + len("psycopg2.errors.")
        #error_message = (traceback_string[start_index:]).lstrip().replace('\n',
        #                                                                  ' ')  # lstrip() entfernt Anfangsleerzeichen

        #with connection.cursor() as error_cursor:
        #    error_cursor.execute("INSERT INTO FehlerLog (FehlerNachricht) VALUES (%s)", (error_message,))
        #    connection.commit()
        print("Error:", error_message)  # Fehler in Console
        # traceback.print_exc() #ausfuerhlicher Fehler
        #continue

connection.commit()
fuzzy_cursor.close()
connection.close()

"""
select * from autor INNER JOIN buch_autor 
ON autor.autorid = buch_autor.autorid
INNER JOIN buch ON buch_autor.pid = buch.pid 
INNER JOIN Produkt ON buch_autor.pid = Produkt.pid
where autorname LIKE '%Frhlich%' 
	OR autorname LIKE '%Fröhlich%'
"""


