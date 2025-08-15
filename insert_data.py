import sqlite3
import json

# Load scraped data from JSON
with open("torn_wiki_data_final.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Connect to your existing SQLite database
conn = sqlite3.connect("torn_wiki_data.db")
cursor = conn.cursor()

# Insert data into the table
for item in data:
    cursor.execute("INSERT INTO wiki_data (content) VALUES (?)", (item["content"],))

conn.commit()
conn.close()

print("✅ Data inserted successfully into the existing database!")
