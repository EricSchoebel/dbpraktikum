/*
Abgabe Teil 2b i - Datei mit SQL-Statements für ein ausgewähltes Beispiel
(Hinweis: die Trigger mit Funktion stehen in "Abgabe2b_ii.sql",
 Screenshots für den kompletten Testfall im Ordner "Screenshots_2b_i")
Es wird eine Test-Kundenrezension verfasst, um zu prüfen ob sich das entsprechende Rating für dieses Produkt anpasst.

Bezug wird auf das folgendes Produkt aus der Produkt-Tabelle genommen (Stand vor dem Test):
pid: 3473530190
titel: Englisch lernen mit Witzen
rating: 4.5

Dieses Produkt hat vor dem Test 2 Kundenrezensionen, eine mit 4 Punkten, die andere mit 5 Punkten ( Rating = (4+5)/2 ).

Test-Szenario Reihenfolge:

a) INSERT-Fall: neue Test-Kundenrezension zum Produkt wird in Kundenrezension-Tabelle eingefügt (mit Punktewert 1)
                -> Rating in Produkt-Tabelle sollte damit unter 4,5 und zwar auf 3,3 (=10/3) gehen

b) UPDATE-FALL: zuvor eingefügte Test-Kundenrezension zum Produkt wird angepasst (mit Punktewert 5)
                -> Rating in Produkt-Tabelle sollte damit über 4,5 und zwar auf 4,7 (=14/3) werden

c) DELETE-FALL1 (EINE Löschung): eingefügte Test-Kundenrezension wird wieder gelöscht
                -> Rating in Produkt-Tabelle sollte auf 4,5 zurückgehen

d) DELETE-FALL2 (MEHRFACHE Löschung): eingefügte Test-Kundenrezension (mit 5 Punkten) wird wieder hergestellt,
                um dann selbige und die andere Rezension mit 5 Punkten (vom Kunden "thegreatmm") zu löschen
                -> es verbleibt nur noch die Rezension mit 4 Punkten
                -> Rating in Produkt-Tabelle sollte zu 4 werden

e) DELETE-Fall3 (ALLE Kundenrezensionen zu diesem Produkt werden gelöscht):
                die Test-Kundenrezension mit 5 Punkten wird wieder hergestellt 
                (es sind nun also wieder zwei Rezensionen, mit 4 und 5 Punkten, vorhanden),
                nun werden alle Rezensionen zu dem Produkt gelöscht
                -> Rating in Produkt-Tabelle sollte zu NULL werden

-> Nach dem Testen ist ein erneutes Beladen der DB mit Importskript notwendig, 
   um wieder den alten Stand vor dem Test zu erhalten
)  
*/

--vor dem Test:
SELECT * FROM Kundenrezension WHERE PID = '3473530190';
SELECT pid, titel, rating FROM Produkt WHERE PID = '3473530190';
/* Rating ist 4.5 */

--- a)
INSERT INTO Kunde (KundenID, Kundenname) VALUES ('123456789', 'Test'); --ohne Kunden kann man keine Rezension anlegen
INSERT INTO Kundenrezension (KundenID, PID, Punkte) VALUES ('123456789', '3473530190', 1); --mit 1 Punkt eingefügt
SELECT pid, titel, rating FROM Produkt WHERE PID = '3473530190'; --Überprüfung ob geklappt
/*Ergebnis: Rating ist nun 3.3 -> es hat geklappt */

--- b)
UPDATE Kundenrezension
SET Punkte = 5
WHERE KundenID = '123456789' AND PID = '3473530190';
SELECT pid, titel, rating FROM Produkt WHERE PID = '3473530190';
/*Ergebnis: Rating ist nun 4.7 -> es hat geklappt */

--- c)
DELETE FROM Kundenrezension WHERE KundenID = '123456789' AND PID = '3473530190';
SELECT pid, titel, rating FROM Produkt WHERE PID = '3473530190'; 
/*Ergebnis: Rating ist wieder 4.5 -> es hat geklappt */

--- d)
INSERT INTO Kundenrezension (KundenID, PID, Punkte) VALUES ('123456789', '3473530190', 5); --mit 5 Punkten eingefügt
DELETE FROM Kundenrezension WHERE (KundenID='123456789' OR KundenID='thegreatmm') AND PID = '3473530190';
SELECT pid, titel, rating FROM Produkt WHERE PID = '3473530190'; 
/*Ergebnis: Rating ist wieder 4.0 -> es hat geklappt */

--- e)
INSERT INTO Kundenrezension (KundenID, PID, Punkte) VALUES ('123456789', '3473530190', 5); --mit 5 Punkten eingefügt
DELETE FROM Kundenrezension WHERE PID = '3473530190';
DELETE FROM Kunde WHERE KundenID = '123456789';
SELECT pid, titel, rating FROM Produkt WHERE PID = '3473530190';
/*Ergebnis: Rating ist null -> es hat geklappt */

