# Relational Database Interneship
## Development of a Database Application


by Eric Schöbel and Jan Schlenker

The present project was carried out as part of the module "Relational Database Internship" in the Computer Science program at the University of Leipzig. It received an overall grade of 1.0 (the best grade in Germany).

A complete database application was developed. A **Postgres** database, along with **pgAdmin** as a GUI, was set up using **Docker**. **XML** and **CSV** data can be loaded into the database using a **Python** import script, and potentially erroneous data is filtered out, for example, through fuzzy matching.

The backend was programmed in **Java** using **Spring**. Hibernate, through Spring Data JPA, was used for Object-Relational Mapping (ORM).

Communication between the backend and frontend is facilitated through a REST API. In a Dockerized form, **Vue.js 3** with **Vuetify 3** was used for the frontend.

To start the program, bring up the Docker containers using the docker-compose.yml file in the terminal with "docker-compose up -d." Run the Spring application locally and follow the instructions. Then, access it in a web browser at localhost:8081. When using it for the first time, load the data into the database using the import script.
