#Vorbemerkung: postgres-DockerContainer must be up

# in terminal: pip install psycopg2
import psycopg2 #Psycopg is the most popular PostgreSQL database adapter for Python

try:
    connection = psycopg2.connect(
        host="localhost",
        port="6432", # hier 6432 weil ich die Portbindung geändert hatte
        database="dbprak_postgres",
        user="dbprak_postgres",
        password="dbprak_postgres"
    )

    # Perform database operations here
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM friendship") # friendship war die Beispieltabelle, die ich angelegt hatte
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()

except psycopg2.Error as error:
    print("Error connecting to PostgreSQL:", error)

connection.close()





#if __name__ == '__main__':
#    print(Hi)
