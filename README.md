# Relationales Datenbankpraktikum
## Entwicklung einer Datenbankanwendung


von Eric Schöbel und Jan Schlenker

Das vorliegende Projekt entstand im Rahmen des Moduls *"Relationales Datenbankpraktikum"* im Studiengang Informatik der Universität Leipzig. Es wurde insgesamt mit einer 1,0 (beste deutsche Note) bewertet. 

Entwickelt wurde eine vollständige Datenbank-Anwendung. Mithilfe von **Docker** wurde eine **Postgres**-Datenbank plus **pgAdmin** als GUI aufgesetzt. Über ein in **Python** geschriebenes Importskript können **XML**- und **CSV**-Daten in die Datenbank hineingeladen werden. Dabei werden potenziell fehlerhafte Daten bspw. über Fuzzy Matching herausgefiltert. 

Das Backend wurde in **Java** mithilfe von **Spring** progammiert. Für das Objektrelationale Mapping (ORM) wurde dabei insbesondere Hibernate über die Spring Data JPA genutzt. 

Über eine REST-API wird die Kommunikation zwischen Backend und Frontend dargestellt. Für das Frontend wurde in dockerisierter Form **Vue.js 3** mit **Vuetify 3** verwendet.

Zum Starten des Programms die Docker-Container über die docker-compose.yml im Terminal via "docker-compose up -d" hochfahren. Die Spring-Anwendung lokal ausführen und den Anweisungen folgen. Dann im Webbrowser auf localhost:8081 gehen. Bei erstmaliger Nutzung die Daten über das Importskript in die Datenbank laden.
