/*
Abgabe Teil 2b ii - Datei mit Anweisungen zur Integritätssicherung
*/

-- Ausschnitt der relevanten Tabellen aus Datenbank-Schema:

CREATE TABLE Produkt (
  PID VARCHAR(20) PRIMARY KEY,
  Titel VARCHAR(255),
  Rating DECIMAL(2,1),
  Verkaufsrang INT,
  Bild BYTEA
);
CREATE INDEX verkaufsrang_index ON Produkt(verkaufsrang);

CREATE TABLE Kundenrezension (
	KundenID varchar(100),
	PID VARCHAR(20),
	Punkte INT CHECK (Punkte BETWEEN 1 AND 5),
	Helpful INT,
	Summary TEXT,
	Content TEXT,
	Reviewdate DATE,
	PRIMARY KEY (KundenID, PID),
	FOREIGN KEY (KundenID) REFERENCES Kunde(KundenID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (PID) REFERENCES Produkt(PID) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX rezension_rd_index ON Kundenrezension(Reviewdate); 
CREATE INDEX helpful_index ON Kundenrezension(Helpful); 
CREATE INDEX punkte_index ON Kundenrezension(Punkte); 

/* Erklärung: 
In Produkt-Tabelle gibt der Datentyp "DECIMAL(2,1)" bei Rating an, dass das Rating eine Dezimalzahl ist,
die insgesamt 2 Ziffern enthält, wobei eine Ziffer für den Dezimalteil reserviert ist.
Das bedeutet, dass das Rating Werte wie z.B. 3.5, 4.0, 2.9 usw. haben kann.

Das Rating speist sich aus der durchschnittlichen Punktzahl der zugehörigen Kundenrezensionen aus der
Kundenrezension-Tabelle. Der CHECK bei Punkte sichert ab, dass nur ganzzahlige Punktewerte von 1 bis 5 vergeben werden.
Damit wird implizit auch der Wertebereich für das Rating in der Produkt-Tabelle festgelegt.

Die letztlich bestehende Verbindung der Tabellenwerte wurde über Trigger realisiert. 
Im speziellen wurde eine Funktion definiert, die bei Auslösung der eigentlichen Trigger ausgeführt wird.
Die Auslösung erfolgt sowohl nach dem INSERT, UPDATE als auch DELETE in der Kundenrezension-Tabelle.
Da der DELETE-Fall einer anderen Logik bedarf, wurde dafür eine andere Funktion angelegt.
Die Realisierung geschah wie folgt:
*/

--Funktion für INSERT und UPDATE
CREATE OR REPLACE FUNCTION UpdateRatingFunction()
RETURNS TRIGGER AS
$BODY$
BEGIN
	UPDATE Produkt
	SET Rating = (SELECT AVG(Punkte) FROM Kundenrezension WHERE PID = NEW.PID)
	WHERE PID = NEW.PID;
	RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql;

--ACHTUNG: funktionsdefinition für delete case noch einfuegen

CREATE TRIGGER UpdateRating_Insert
AFTER INSERT ON Kundenrezension
FOR EACH ROW
EXECUTE FUNCTION UpdateRatingFunction();

CREATE TRIGGER UpdateRating_Update
AFTER UPDATE ON Kundenrezension
FOR EACH ROW
EXECUTE FUNCTION UpdateRatingFunction();


--ACHTUNG hier wird eine andere Fkt aufgerfuen
CREATE TRIGGER UpdateRating_Delete
AFTER DELETE ON Kundenrezension
FOR EACH ROW
EXECUTE FUNCTION DeleteCaseUpdateRatingFunction();


