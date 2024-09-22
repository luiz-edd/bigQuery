import requests
import psycopg2

# Fetching Pokemon data
r = requests.get('https://pokeapi.co/api/v2/pokemon?offset=20&limit=10000')
r_js = r.json()

i = 0
pokelist = []
for var in r_js.get("results"):
    pokedict = {}
    pokedict["id"] = i + 1  # Assign ID starting from 1
    pokedict["name"] = var["name"]
    info_request = requests.get(var.get("url"))
    info_data = info_request.json()
    info_species = (requests.get(info_data.get("species").get("url"))).json()
    
    print(f"Fetching data for: {pokedict['name']}")
    
    # Add type with protection
    pokedict["type"] = info_data.get("types")[0].get("type").get("name") if len(info_data.get("types", [])) > 0 else None
    
    # Add height and weight
    pokedict["height"] = info_data.get("height")
    pokedict["weight"] = info_data.get("weight")
    
    # Add experience, capture rate, base happiness
    pokedict["base_experience"] = info_species.get("base_happiness")
    pokedict["capture_rate"] = info_species.get("capture_rate")
    pokedict["base_happiness"] = info_data.get("base_experience")
    
    # Add color with protection
    pokedict["color"] = info_species.get("color", {}).get("name")
    
    # Add egg groups with protection
    egg_groups = info_species.get("egg_groups", [])
    pokedict["egg_group_01"] = egg_groups[0].get("name") if len(egg_groups) > 0 else None
    pokedict["egg_group_02"] = egg_groups[1].get("name") if len(egg_groups) > 1 else None
    
    # Add generation with protection
    pokedict["generation"] = info_species.get("generation", {}).get("name")
    
    # Add held items with protection
    pokedict["held_items"] = info_data.get("held_items")[0].get("item").get("name") if len(info_data.get("held_items", [])) > 0 else None
    
    # Add moves with protection
    pokedict["move_01"] = info_data.get("moves")[0].get("move").get("name") if len(info_data.get("moves", [])) > 0 else None
    pokedict["move_02"] = info_data.get("moves")[1].get("move").get("name") if len(info_data.get("moves", [])) > 1 else None
    pokedict["move_03"] = info_data.get("moves")[2].get("move").get("name") if len(info_data.get("moves", [])) > 2 else None
    
    pokelist.append(pokedict)
    i += 1
    if i == 1000:  # Adjust if needed
        break

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123",
    host="172.18.0.3",
    port="5432"
)
cursor = conn.cursor()

# Create table if it doesn't exist with the new columns
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        type VARCHAR(50),
        height INTEGER,
        weight INTEGER,
        base_experience INTEGER,
        capture_rate INTEGER,
        base_happiness INTEGER,
        color VARCHAR(50),
        egg_group_01 VARCHAR(50),
        egg_group_02 VARCHAR(50),
        generation VARCHAR(50),
        held_items VARCHAR(50),
        move_01 VARCHAR(50),
        move_02 VARCHAR(50),
        move_03 VARCHAR(50),
        UNIQUE (id)
    );
""")

# Insert data into PostgreSQL with the new fields
for poke in pokelist:
    cursor.execute(
        """
        INSERT INTO pokemon (id, name, type, height, weight, base_experience, capture_rate, base_happiness, color, egg_group_01, egg_group_02, generation, held_items, move_01, move_02, move_03)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        """,
        (poke['id'], poke['name'], poke['type'], poke.get('height'), poke.get('weight'), poke.get('base_experience'), poke.get('capture_rate'), poke.get('base_happiness'), poke.get('color'), poke.get('egg_group_01'), poke.get('egg_group_02'), poke.get('generation'), poke.get('held_items'), poke.get('move_01'), poke.get('move_02'), poke.get('move_03'))
    )

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
