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

CREATE TABLE Buch (
  PID VARCHAR(20) PRIMARY KEY,
  Seitenzahl INT,
  Erscheinungsdatum DATE,
  ISBN VARCHAR(255),
  Verlag VARCHAR(255),
  FOREIGN KEY (PID) REFERENCES Produkt(PID)
);

CREATE TABLE DVD (
  PID VARCHAR(20) PRIMARY KEY,
  Format VARCHAR(255),
  Laufzeit INT,
  Regioncode VARCHAR(255),
  FOREIGN KEY (PID) REFERENCES Produkt(PID)
);

CREATE TABLE CD (
  PID VARCHAR(20) PRIMARY KEY,
  Label VARCHAR(255),
  Erscheinungsdatum DATE,
  FOREIGN KEY (PID) REFERENCES Produkt(PID),
  CONSTRAINT CD_Kuenstler_PID_fk FOREIGN KEY (PID) REFERENCES Produkt(PID)
);

CREATE TABLE Autor (
  AutorID INT PRIMARY KEY,
  Autorname VARCHAR(255)
);


CREATE TABLE Buch_Autor (
  PID VARCHAR(20),
  AutorID INT,
  PRIMARY KEY (PID, AutorID),
  FOREIGN KEY (PID) REFERENCES Buch(PID),
  FOREIGN KEY (AutorID) REFERENCES Autor(AutorID)
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
  FOREIGN KEY (PID) REFERENCES DVD(PID),
  FOREIGN KEY (BeteiligtenID) REFERENCES DVD_Beteiligte(BeteiligtenID)
);

CREATE TABLE Kuenstler (
  KuenstlerID INT PRIMARY KEY,
  Kuenstlername VARCHAR(255) NOT NULL
);

CREATE TABLE CD_Kuenstler (
  PID VARCHAR(20),
  KuenstlerID INT,
  PRIMARY KEY (PID, KuenstlerID),
  FOREIGN KEY (PID) REFERENCES CD(PID),
  FOREIGN KEY (KuenstlerID) REFERENCES Kuenstler(KuenstlerID)
);


CREATE TABLE Titel (
  PID VARCHAR(20),
  Titelname VARCHAR(255),
  PRIMARY KEY(PID, Titelname),
  FOREIGN KEY (PID) REFERENCES CD(PID)
);

CREATE TABLE Kategorie (
  KatID INT PRIMARY KEY,
  Kategoriename VARCHAR(255),
  Oberkategorie INT,
  FOREIGN KEY (Oberkategorie) REFERENCES Kategorie(KatID)
);

CREATE TABLE Produkt_Kategorie (
  KatID INT,
  PID VARCHAR(20),
  PRIMARY KEY (KatID, PID),
  FOREIGN KEY (KatID) REFERENCES Kategorie(KatID),
  FOREIGN KEY (PID) REFERENCES Produkt(PID)
);

CREATE TABLE Filiale (
  FID INT PRIMARY KEY,
  Filialname VARCHAR(255)
);

CREATE TABLE Anschrift (
  FID INT PRIMARY KEY,
  Strasse VARCHAR(255),
  Hausnummer VARCHAR(255),
  PLZ VARCHAR(255),
  FOREIGN KEY (FID) REFERENCES Filiale(FID),
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
	Preis DECIMAL(10,2),
	Zustandsnummer INT,
	Menge INT,
	FOREIGN KEY (PID) REFERENCES Produkt(PID),
	FOREIGN KEY (FID) REFERENCES Filiale(FID),
	FOREIGN KEY (Zustandsnummer) REFERENCES Zustand(Zustandsnummer),
	CONSTRAINT unique_offer_constraint UNIQUE (PID, FID, Preis, Zustandsnummer)
);

CREATE TABLE Kunde (
	KundenID varchar(100) PRIMARY KEY
);

CREATE TABLE Konto (
    	KundenID varchar(100),
Kontonummer INT,
    	PRIMARY KEY(KundenID, Kontonummer),
	FOREIGN KEY (KundenID) REFERENCES Kunde(KundenID)
);

CREATE TABLE Lieferadresse (
	KundenID varchar(100),
	Strasse VARCHAR(100),
	Hausnummer VARCHAR(10),
	PLZ VARCHAR(10),
	FOREIGN KEY (KundenID) REFERENCES Kunde(KundenID)
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
	FOREIGN KEY (KundenID) REFERENCES Kunde(KundenID),
	FOREIGN KEY (PID) REFERENCES Produkt(PID)
);

CREATE OR REPLACE FUNCTION UpdateRatingFunction()
RETURNS TRIGGER AS $$
BEGIN
	UPDATE Produkt
	SET Rating = (SELECT AVG(Punkte) FROM Kundenrezension WHERE PID = NEW.PID)
	WHERE PID = NEW.PID;
    
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER UpdateRating
AFTER INSERT ON Kundenrezension
FOR EACH ROW
EXECUTE FUNCTION UpdateRatingFunction();

CREATE TABLE Kauf (
	AngebotsID INT,
	KundenID varchar(100),
	Menge INT,
	Zeitpunkt TIMESTAMP,
	PRIMARY KEY (KundenID, AngebotsID, Zeitpunkt),
	FOREIGN KEY (KundenID) REFERENCES Kunde(KundenID),
	FOREIGN KEY (AngebotsID) REFERENCES Angebot(AngebotsID)
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
	/* Aehnlichkeitswert DECIMAL(10,2), */
	PRIMARY KEY (PID1, PID2),
	FOREIGN KEY (PID1) REFERENCES Produkt(PID),
	FOREIGN KEY (PID2) REFERENCES Produkt(PID),
	CHECK (compare_strings_less_than(PID1, PID2))
);




'''