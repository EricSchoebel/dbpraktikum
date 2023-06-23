#drop all tables
sql_drop_tables = '''DROP SCHEMA public CASCADE;
CREATE SCHEMA public;'''

#all create-statements as one string
sql_creates = '''CREATE TABLE FehlerLog (
    FehlerID SERIAL PRIMARY KEY,
    FehlerNachricht TEXT
);


CREATE TABLE Produkt (
  PID VARCHAR(20) PRIMARY KEY,
  Titel VARCHAR(255),
  Rating DECIMAL(2,1),
  Verkaufsrang INT,
  Bild BYTEA
);
CREATE INDEX verkaufsrang_index ON Produkt(verkaufsrang); /*schnelleres Abgleichen und Sortieren*/
/*kein Index auf Rating wegen häufiger Updates (sonst schlechtere performance)*/


CREATE TABLE Buch (
  PID VARCHAR(20) PRIMARY KEY,
  Seitenzahl INT,
  Erscheinungsdatum DATE,
  ISBN VARCHAR(255),
  Verlag VARCHAR(255),
  FOREIGN KEY (PID) REFERENCES Produkt(PID) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX seitenzahl_index ON Buch(seitenzahl); /*schnelleres Abgleichen und Sortieren*/
CREATE INDEX buch_rd_index ON Buch(erscheinungsdatum); /*schnelleres Abgleichen und Sortieren*/

CREATE TABLE DVD (
  PID VARCHAR(20) PRIMARY KEY,
  Format VARCHAR(255),
  Laufzeit INT,
  Regioncode VARCHAR(255),
  FOREIGN KEY (PID) REFERENCES Produkt(PID) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX laufzeit_index ON DVD(laufzeit); /*schnelleres Abgleichen und Sortieren*/

CREATE TABLE CD (
  PID VARCHAR(20) PRIMARY KEY,
  Label VARCHAR(255),
  Erscheinungsdatum DATE,
  FOREIGN KEY (PID) REFERENCES Produkt(PID) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT CD_Kuenstler_PID_fk FOREIGN KEY (PID) REFERENCES Produkt(PID)
);
CREATE INDEX CD_rd_index ON CD(erscheinungsdatum); /*schnelleres Abgleichen und Sortieren*/

CREATE TABLE Autor (
  AutorID INT PRIMARY KEY,
  Autorname VARCHAR(255)
);
CREATE INDEX autorname_index ON Autor(Autorname); /*schnelleres Abgleichen und Selektieren*/


CREATE TABLE Buch_Autor (
  PID VARCHAR(20),
  AutorID INT,
  PRIMARY KEY (PID, AutorID),
  FOREIGN KEY (PID) REFERENCES Buch(PID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (AutorID) REFERENCES Autor(AutorID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE DVD_Beteiligte (
  BeteiligtenID INT PRIMARY KEY,
  Beteiligtenname VARCHAR(255)
);

CREATE TABLE DVD_Beteiligungen (
  PID VARCHAR(20),
  BeteiligtenID INT,
  Rolle VARCHAR(255),
  PRIMARY KEY (PID, BeteiligtenID, Rolle),
  FOREIGN KEY (PID) REFERENCES DVD(PID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (BeteiligtenID) REFERENCES DVD_Beteiligte(BeteiligtenID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Kuenstler (
  KuenstlerID INT PRIMARY KEY,
  Kuenstlername VARCHAR(255) NOT NULL
);
CREATE INDEX kuenstlername_index ON kuenstler(kuenstlername); /*schnelleres Abgleichen und Selektieren*/

CREATE TABLE CD_Kuenstler (
  PID VARCHAR(20),
  KuenstlerID INT,
  PRIMARY KEY (PID, KuenstlerID),
  FOREIGN KEY (PID) REFERENCES CD(PID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (KuenstlerID) REFERENCES Kuenstler(KuenstlerID) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE Titel (
  PID VARCHAR(20),
  Titelname VARCHAR(255),
  PRIMARY KEY(PID, Titelname),
  FOREIGN KEY (PID) REFERENCES CD(PID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Kategorie (
  KatID INT PRIMARY KEY,
  Kategoriename VARCHAR(255),
  Oberkategorie INT,
  FOREIGN KEY (Oberkategorie) REFERENCES Kategorie(KatID) ON UPDATE CASCADE ON DELETE CASCADE
);
/* Index auf Oberkategorie ? -> viele Dopplungen, aber viel Filtern*/ 

CREATE TABLE Produkt_Kategorie (
  KatID INT,
  PID VARCHAR(20),
  PRIMARY KEY (KatID, PID),
  FOREIGN KEY (KatID) REFERENCES Kategorie(KatID) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (PID) REFERENCES Produkt(PID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Filiale (
  FID INT PRIMARY KEY,
  Filialname VARCHAR(255)
);
CREATE INDEX filialname_index ON Filiale(Filialname); /*schnelleres Abgleichen und Selektieren*/

CREATE TABLE Anschrift (
  FID INT PRIMARY KEY,
  Strasse VARCHAR(255),
  Hausnummer VARCHAR(255),
  PLZ VARCHAR(255),
  FOREIGN KEY (FID) REFERENCES Filiale(FID) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT Anschrift_FID_unique UNIQUE (FID)
);

CREATE TABLE Zustand (
  Zustandsnummer SERIAL PRIMARY KEY,
  Beschreibung VARCHAR(255)
);

CREATE TABLE Angebot (
	AngebotsID INT PRIMARY KEY,
	PID VARCHAR(20),
	FID INT,
	Preis DECIMAL(10,2) CHECK (Preis >= 0), /* wie in Testat besprochen */
	Zustandsnummer INT,
	Menge INT,
	FOREIGN KEY (PID) REFERENCES Produkt(PID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (FID) REFERENCES Filiale(FID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Zustandsnummer) REFERENCES Zustand(Zustandsnummer) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT unique_offer_constraint UNIQUE (PID, FID, Preis, Zustandsnummer)
);
CREATE INDEX preis_index ON Angebot(Preis); /*schnelleres Abgleichen und Sortieren*/
CREATE INDEX pid_index ON Angebot(PID); /*schnellere JOINs*/
CREATE INDEX fid_index ON Angebot(FID); /*schnellere JOINs*/

CREATE TABLE Kunde (
	KundenID varchar(100) PRIMARY KEY,
	Kundenname VARCHAR(100)
);

CREATE TABLE Konto (
    	KundenID varchar(100),
        Kontonummer INT,
    	PRIMARY KEY(KundenID, Kontonummer),
	FOREIGN KEY (KundenID) REFERENCES Kunde(KundenID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Lieferadresse (
	KundenID varchar(100),
	Strasse VARCHAR(100),
	Hausnummer VARCHAR(10),
	PLZ VARCHAR(10),
	FOREIGN KEY (KundenID) REFERENCES Kunde(KundenID) ON UPDATE CASCADE ON DELETE CASCADE
);

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
CREATE INDEX rezension_rd_index ON Kundenrezension(Reviewdate); /*schnelles Abgleichen und Sortieren*/
CREATE INDEX helpful_index ON Kundenrezension(Helpful); /*schnelles Abgleichen und Sortieren*/
CREATE INDEX punkte_index ON Kundenrezension(Punkte); /*schnelles Abgleichen und Sortieren*/

--Funktion fuer INSERT und UPDATE Fälle
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

--Funktion fuer DELETE Fälle
CREATE OR REPLACE FUNCTION DeleteCaseUpdateRatingFunction()
RETURNS TRIGGER AS 
$BODY$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM Kundenrezension
        WHERE PID = OLD.PID
          AND KundenID <> OLD.KundenID
    ) THEN
        UPDATE Produkt
        SET Rating = NULL -- oder setzen Sie hier den gewünschten Standardwert
        WHERE PID = OLD.PID;
    ELSE
        UPDATE Produkt
        SET Rating = (
            SELECT AVG(Punkte)
            FROM Kundenrezension
            WHERE PID = OLD.PID
              AND KundenID <> OLD.KundenID
        )
        WHERE PID = OLD.PID;
    END IF;
    RETURN NULL; 
END;
$BODY$
LANGUAGE plpgsql;

CREATE TRIGGER UpdateRating_Insert
AFTER INSERT ON Kundenrezension
FOR EACH ROW
EXECUTE FUNCTION UpdateRatingFunction();

CREATE TRIGGER UpdateRating_Update
AFTER UPDATE ON Kundenrezension
FOR EACH ROW
EXECUTE FUNCTION UpdateRatingFunction();

CREATE TRIGGER UpdateRating_Delete
AFTER DELETE ON Kundenrezension
FOR EACH ROW
EXECUTE FUNCTION DeleteCaseUpdateRatingFunction();

CREATE TABLE Kauf (
	AngebotsID INT,
	KundenID varchar(100),
	Menge INT,
	Zeitpunkt TIMESTAMP,
	PRIMARY KEY (KundenID, AngebotsID, Zeitpunkt),
	FOREIGN KEY (KundenID) REFERENCES Kunde(KundenID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (AngebotsID) REFERENCES Angebot(AngebotsID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION compare_strings_less_than(text, text)
  RETURNS boolean AS
$$
BEGIN
  RETURN $1 < $2;
END;
$$
LANGUAGE plpgsql;

CREATE TABLE Aehnlichkeit (
	PID1 VARCHAR(20),
	PID2 VARCHAR(20),
	PRIMARY KEY (PID1, PID2),
	FOREIGN KEY (PID1) REFERENCES Produkt(PID) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (PID2) REFERENCES Produkt(PID) ON UPDATE CASCADE ON DELETE CASCADE,
	CHECK (compare_strings_less_than(PID1, PID2))
);





'''