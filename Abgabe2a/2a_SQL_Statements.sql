--1.)
SELECT (SELECT COUNT(*) FROM Buch) AS BuchAnzahl, (SELECT COUNT(*) FROM CD) AS MusikCDAnzahl, (SELECT COUNT(*) FROM DVD) AS DVDAnzahl
--Hinweis: in Postgres funktioniert das so ohne FROM-Klausel

--2.)
WITH buchabfrage AS (
	SELECT 'Buch' AS Typ, pid AS ProduktNr, rating AS Rating
	FROM BUCH NATURAL JOIN Produkt
	WHERE rating IS NOT NULL 
	ORDER BY rating DESC
	LIMIT 5
    ),
	musikcdabfrage AS (
	SELECT 'MusikCD' AS Typ, pid AS ProduktNr, rating AS Rating
	FROM CD NATURAL JOIN Produkt
	WHERE rating IS NOT NULL 
	ORDER BY rating DESC
	LIMIT 5
	),
	dvdabfrage AS (
	SELECT 'DVD' AS Typ, pid AS ProduktNr, rating AS Rating
	FROM DVD NATURAL JOIN Produkt
	WHERE rating IS NOT NULL 
	ORDER BY rating DESC
    LIMIT 5
	)
SELECT Typ, ProduktNr, Rating FROM		
		 (SELECT * FROM buchabfrage 
	  	 UNION ALL SELECT * FROM musikcdabfrage
      	 UNION ALL SELECT * FROM dvdabfrage) AS hilfs
ORDER BY hilfs.Rating DESC

--3.)
SELECT p.pid FROM Produkt p
WHERE p.pid NOT IN (SELECT pid FROM angebot a WHERE a.menge > 0)

--4.)
SELECT p.PID
FROM Produkt p
INNER JOIN Angebot a ON p.PID = a.PID
GROUP BY p.PID
HAVING MAX(a.Preis) > 2 * MIN(a.Preis);

--5.) "sowohl als auch"-Fall (Schnitt)
SELECT pid FROM Kundenrezension WHERE punkte=1
INTERSECT
SELECT pid FROM Kundenrezension WHERE punkte=5

--6.) “alle, die keine”-Fall (Differenz)
SELECT COUNT(*) AS Produktanzahl_Ohne_Rezension FROM
    (SELECT p.pid FROM Produkt p
     EXCEPT
     SELECT k.pid FROM Kundenrezension k) AS differenz

--7.)
SELECT kundenid FROM kundenrezension
GROUP BY kundenid
HAVING COUNT(*)>=10
ORDER BY COUNT(*) DESC

--8.)
SELECT DISTINCT a.autorname FROM autor a
WHERE a.autorid IN (
    SELECT ba.autorid FROM buch_autor ba
    INTERSECT SELECT ck.kuenstlerid FROM cd_kuenstler ck
    INTERSECT SELECT dvdb.beteiligtenid FROM dvd_beteiligte dvdb
    ) 
ORDER BY a.autorname ASC

--9.)
SELECT (sum(absolutwerte_liederanzahl)/count(*)) AS durchschnitt_liederanzahl 
FROM (SELECT t.pid, count(*) AS absolutwerte_liederanzahl from titel t
    	    GROUP BY t.pid) anzahlliste

--10.)
/* Vorüberlegung: es muss grundsätzlich entschieden werden, ob ein Produkt änhlich zu sich selbst ist?

Falls nein: Variante "ohne ähnlich zu sich selbst" (umgangssprachlich interessante Variante) (= Variante 1)
Falls ja: Variante "mit ähnlich zu sich selbst" (mathematisch korrekte Variante) (= Variante 2)

Grundlegender Unterschied ist, dass in der zweiten Variante auch die Produkte aufgenommen werden, die selbst in mehreren
Hauptkategorien liegen.
 */

--VARIANTE 1
 WITH rekursiverHauptkatFinder as (
				WITH RECURSIVE Vorfahren (katid, vorfahr, generation) AS
				( SELECT katid, oberkategorie, 1
					FROM kategorie
					UNION
					SELECT V.katid, E.oberkategorie, V.Generation+1
					FROM Vorfahren V, kategorie E
					WHERE V.vorfahr = E.katid)
				SELECT katid, generation, vorfahr FROM Vorfahren
				WHERE katid IN (SELECT h.katid FROM kategorie h) --man will ja für alle katids die zugehörige hauptkategorie
				AND vorfahr IN (SELECT DISTINCT M.katid FROM kategorie M where oberkategorie IS NULL) --uns interessiert ja bloss der "oberste" Vorfahr (aka Hauptkategorie)
				--AND katid IN (29) --hier könnte man spezielle katid eingeben für die man die Hauptkategorie möchte
				),
		zuordnungstabelle as ( --in ordentliche Mappingtabelle
				select katid as argument_kat, vorfahr as hauptkategorie from rekursiverHauptkatFinder --count(argument_kat) = count(distinct argument_kat)
				),
		/* Hinweis: ein Produkt kann ja in mehreren Kategorien liegen (deswegen ja n:m Tabelle produkt_kategorie)
 		und damit ja auch in potenziell mehreren Hauptkategorien */ 
		produkteMitHauptkat as( --ist jetzt quasi eine neue n:m Tabelle für Produkt und HAUPTkategorie
					SELECT DISTINCT pid, hauptkategorie FROM zuordnungstabelle z INNER JOIN produkt_kategorie pk ON z.argument_kat=pk.katid
					--DISTINCT um gleiche Infos nicht mehrfach zu speichern 
				),
		/* Ab jetzt werden die Infos in einer Tabelle gesammelt */ 
		aehnlichkeitInRedundanterVersion AS (
				SELECT pid1 AS part1, pid2 AS part2 FROM aehnlichkeit
				UNION ALL
				SELECT pid2 AS part1, pid1 AS part2 FROM aehnlichkeit --die andere Richtung noch angefuegt
				),
		aehnlichkeitInRedundanterVersionMitHauptkategorieInfoPart1 AS (
				SELECT part1, part2, hauptkategorie AS hkat1 FROM aehnlichkeitInRedundanterVersion air INNER JOIN produkteMitHauptkat pmk ON air.part1=pmk.pid
				),
		aehnlichkeitInRedundanterVersionMitHauptkategorieInfoPart1UndPart2 AS (
				SELECT part1, part2, hkat1, hauptkategorie AS hkat2 FROM aehnlichkeitInRedundanterVersionMitHauptkategorieInfoPart1 basis INNER JOIN produkteMitHauptkat zusatz ON basis.part2=zusatz.pid
				),
		/* Jetzt hat man die Ähnlichkeit und die Infos zu Hauptkategorien (hkat1 für part1, kat2 für part2) in einer Tabelle vorliegen) */
		antwortFrage10 AS (
				SELECT part1 AS pids_AntwortFrage10 FROM aehnlichkeitInRedundanterVersionMitHauptkategorieInfoPart1UndPart2
				WHERE 1=1 
					AND part1 <> part2 --hier steckt ANDERES ähnliches Produkt drin
					AND hkat1 <> hkat2 --andere Hauptkategorie
				)			
SELECT DISTINCT pids_AntwortFrage10 FROM antwortFrage10;

------

-- Variante 2
WITH rekursiverHauptkatFinder as (
				WITH RECURSIVE Vorfahren (katid, vorfahr, generation) AS
				( SELECT katid, oberkategorie, 1
					FROM kategorie
					UNION
					SELECT V.katid, E.oberkategorie, V.Generation+1
					FROM Vorfahren V, kategorie E
					WHERE V.vorfahr = E.katid)
				SELECT katid, generation, vorfahr FROM Vorfahren
				WHERE katid IN (SELECT h.katid FROM kategorie h) --man will ja für alle katids die zugehörige hauptkategorie
				AND vorfahr IN (SELECT DISTINCT M.katid FROM kategorie M where oberkategorie IS NULL) --uns interessiert ja bloss der "oberste" Vorfahr (aka Hauptkategorie)
				--AND katid IN (29) --hier könnte man spezielle katid eingeben für die man die Hauptkategorie möchte
				),
		zuordnungstabelle as ( --in ordentliche Mappingtabelle
				select katid as argument_kat, vorfahr as hauptkategorie from rekursiverHauptkatFinder --count(argument_kat) = count(distinct argument_kat)
				),
		/* Hinweis: ein Produkt kann ja in mehreren Kategorien liegen (deswegen ja n:m Tabelle produkt_kategorie)
 		und damit ja auch in potenziell mehreren Hauptkategorien */ 
		produkteMitHauptkat as( --ist jetzt quasi eine neue n:m Tabelle für Produkt und HAUPTkategorie
					SELECT DISTINCT pid, hauptkategorie FROM zuordnungstabelle z INNER JOIN produkt_kategorie pk ON z.argument_kat=pk.katid
					--DISTINCT um gleiche Infos nicht mehrfach zu speichern 
				),
		/* Ab jetzt werden die Infos in einer Tabelle gesammelt */ 
		aehnlichkeitInRedundanterVersion AS (
				SELECT pid1 AS part1, pid2 AS part2 FROM aehnlichkeit
				UNION ALL
				SELECT pid2 AS part1, pid1 AS part2 FROM aehnlichkeit --die andere Richtung noch angefuegt
				),
		aehnlichkeitInRedundanterVersionMitHauptkategorieInfoPart1 AS (
				SELECT part1, part2, hauptkategorie AS hkat1 FROM aehnlichkeitInRedundanterVersion air INNER JOIN produkteMitHauptkat pmk ON air.part1=pmk.pid
				),
		aehnlichkeitInRedundanterVersionMitHauptkategorieInfoPart1UndPart2 AS (
				SELECT part1, part2, hkat1, hauptkategorie AS hkat2 FROM aehnlichkeitInRedundanterVersionMitHauptkategorieInfoPart1 basis INNER JOIN produkteMitHauptkat zusatz ON basis.part2=zusatz.pid
				),
		/* Jetzt hat man die Ähnlichkeit und die Infos zu Hauptkategorien (hkat1 für part1, kat2 für part2) in einer Tabelle vorliegen) */
		teilantwortFrage10 AS (
				SELECT part1 AS teilAntwortFrage10 FROM aehnlichkeitInRedundanterVersionMitHauptkategorieInfoPart1UndPart2
				WHERE 1=1 
					AND part1 <> part2 --hier steckt ANDERES ähnliches Produkt drin
					AND hkat1 <> hkat2 --andere Hauptkategorie
				),			
		ohneAehnlichZuSichSelbst AS (
			SELECT DISTINCT teilAntwortFrage10 FROM teilantwortFrage10
			),
		/* Jetzt noch der ZusatzCheck, ob ein Produkt selbst verschiedene Hauptkategorien hat, und wenn ja die pids in Antwort aufnehmen */
		ProduktZuSichSelbst AS(		
					SELECT pid, a1.hauptkategorie AS EineHauptkategorie, a2.hauptkategorie AS AndereHauptkategorie FROM (produkteMitHauptkat a1 INNER JOIN produkteMitHauptkat a2 USING(pid))
			),
		nurPidsAusProduktZuSichSelbst AS( 
					SELECT DISTINCT pid AS ZweiterTeilAntwortFrage10 FROM ProduktZuSichSelbst
					WHERE EineHauptkategorie <> AndereHauptkategorie
			)
SELECT teilAntwortFrage10 AS pid FROM ohneAehnlichZuSichSelbst
UNION 
SELECT ZweiterTeilAntwortFrage10 AS pid FROM nurPidsAusProduktZuSichSelbst;

--11.) “in allen”-Fall (Division) 
SELECT DISTINCT a.pid
    FROM Angebot a
    WHERE NOT EXISTS (
   	 SELECT * FROM Filiale
   	 WHERE fid NOT IN
   		 ( SELECT a2.fid
   		   FROM Angebot a2
   		   WHERE a2.pid=a.pid
   		 )
    )

--12.)
WITH divisiontsteilElfteFrage AS --die PIDs aus Frage 11
   		 (
   			 SELECT DISTINCT a.pid
   			 FROM Angebot a
   			 WHERE NOT EXISTS (
   				 SELECT * FROM Filiale
   				 WHERE fid NOT IN
   				  ( SELECT a2.fid
   					FROM Angebot a2
   					WHERE a2.pid=a.pid
   				  )
   			 )
   		  ),
   	ProduktMitNiedrigstpreiswert AS --fuer jedes angebotene Produkt Niedrigpreis annotieren
      		 (select pid, min(preis) AS niedrigstpreis
   		  from angebot
   		  group by pid
   		  HAVING min(preis) IS NOT NULL
   		 ),
   	niedrigpreisinfoAnFrage11 AS --Verbindung pid aus Frage 11 und Niedrigpreisinfo
   		 (select p.pid, h.niedrigstpreis
   		  FROM ProduktMitNiedrigstpreiswert h NATURAL JOIN divisiontsteilElfteFrage p
   		 ),
   	niedrigPreisfaelleLeipzig AS --die Faelle, wo Niedrigpreis in Leipzig
   		 ( select j.pid, j.niedrigstpreis from niedrigpreisinfoAnFrage11 j INNER JOIN Angebot o
   		 ON j.pid=o.pid AND j.niedrigstpreis=o.preis
   		 WHERE fid = (SELECT fid FROM Filiale WHERE filialname = 'Leipzig')
   		  )
SELECT ( 100.0 * (SELECT COUNT(DISTINCT e.PID) FROM niedrigPreisfaelleLeipzig e)
   	 / (SELECT COUNT(DISTINCT v.PID) FROM divisiontsteilElfteFrage v) ) AS Prozentualteil


