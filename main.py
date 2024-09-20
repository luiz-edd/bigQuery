import requests
import psycopg2

# Fetching Pokemon data
r = requests.get('https://pokeapi.co/api/v2/pokemon')
r_js = r.json()

i = 0
pokelist = []
for var in r_js.get("results"):
    pokedict = {}
    pokedict["name"] = var["name"]
    info_request = requests.get(var.get("url"))
    pokedict["type"] = info_request.json().get("types")[0].get("type").get("name")
    pokelist.append(pokedict)
    i += 1
    if (i == 50):
        break

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123",
    host="172.25.0.3",
    port="5432"
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        name VARCHAR(50),
        type VARCHAR(50)
    );
""")

# Insert data into PostgreSQL
for poke in pokelist:
    cursor.execute(
        "INSERT INTO pokemon (name, type) VALUES (%s, %s)",
        (poke['name'], poke['type'])
    )

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
