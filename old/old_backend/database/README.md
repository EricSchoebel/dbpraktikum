## Verwendung von PostgreSQL mittels Docker
# IN ANALOGIE AN DBS II  (angepasst Eric). Hier bei DBpraktikum ein paar Namen und Ports geändert.

1. Installieren Sie die Programme `docker` und `docker-compose`
2. Starten Sie den Postgres-Server durch Öffnen einen Terminals in diesem Ordner und ausführen des Befehls `docker-compose up -d`
	* Sollten Sie einen 'permission denied' Error erhalten wenn Sie `docker-compose` nutzen, nutzen Sie `sudo` oder fügen Sie den Nutzer der Docker-Gruppe hinzu (`sudo usermod -aG docker $USER`) und loggen Sie sich aus und wieder ein, bevor Sie es erneut versuchen
3. Das pgAdmin Web-Interface ist nach kurzer Wartezeit im Browser erreichbar unter [http://localhost:6050](http://localhost:6050) (Nutzer: wir13fjs@studserv.uni-leipzig.de / Passwort: dbprak)
4. Fügen Sie in pgAdmin einen neuen Server-Verbindung hinzu. Hostname unserer PostreSQL Instanz ist 'postgres.container'. Nutzer und Passwort sind beide als 'postgres' eingestellt. Am besten 'Passwort speichern' auswählen, denn die gesamte Einrichtung muss nur einmal erfolgen. Beim nächsten Start ist pgAdmin dann direkt wieder mit dem Server verbunden.
5. Nun stehen Ihnen alle Tools von pgAdmin und PostgreSQL zur Verfügung. Eine leere Datenbank 'postgres' ist bereits angelegt und kann nun z.B. über das Query-Tool gefüttert werden. In der Datei 'beispieltabellen.sql' finden Sie beispielhaft Befehle zur Erstellung erster Tabellen. Ihr Fortschritt wird lokal gespeichert und ist beim nächsten Start des Servers wieder verfügbar.
6. Zum Stoppen des Postgres-Servers sobald Sie fertig sind, nutzen Sie den Befehl `docker-compose down`
	* Sollen alle lokal gespeicherten Daten mitgelöscht werden, nutzen Sie stattdessen `docker-compose down -v` (Achtung, falls nötig ein Backup der Datenbanken erstellen!)
7. Damit ist die erste Einrichtung abgeschlossen und Sie brauchen fortan nur noch Schritte 2, 3 und 6, um die Postgres-Datenbank zu nutzen. Natürlich können Sie den Datenbank-Server auch außerhalb von pgAdmin nutzen. Sie ist unter dem Port '5432' erreichbar.


## How to use dockerized PostgreSQL

1. Install `docker` and `docker-compose`
2. Start Postgres server by opening a terminal in this folder and running `docker-compose up -d`
	* If a 'permission denied' error occurs when using `docker-compose`, use `sudo` or add user to docker group (`sudo usermod -aG docker $USER`) and log out and in, before trying again
3. After a short delay, the pgAdmin web interface is available in your browser at [http://localhost:6050](http://localhost:6050) (User: pgadmin@pgadmin.com / Password: pgadmin)
4. Create a new server connection in pgAdmin. Hostname our PostgreSQL instance is 'postgres.container'. User and password are both set to 'postgres'. It is advisable to select 'Save password', because the whole setup process has to be done only once. At the next start, pgAdmin will already be connected to the server.
5. You are now able to use all tools of pgAdmin and PostgreSQL. An empty database 'postgres' is already created and can now be fed e.g. via the query tool. The file 'friend_tables.sql' provides an example for creating your first tables. Your progress is saved locally and will be available the next time you start the server.
6. Stop Postgres server when finished by running `docker-compose down`
	* If all local data should be erased, instead use the following command `docker-compose down -v` (Care, be sure to backup your databases if needed!)
7. This completes the initial setup and from now on you only need steps 2, 3 and 6 to use the Postgres database. Of course you can also use the database server outside of pgAdmin. It is available on port '5432'.
