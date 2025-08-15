import json
import sqlite3

# Load the scraped JSON data
json_filename = "torn_wiki_data_final.json"
with open(json_filename, "r", encoding="utf-8") as file:
    data = json.load(file)

# Connect to SQLite database (or create it)
db_name = "torn_wiki.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS wiki_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        content TEXT
    )
""")

# Insert data into the table
for entry in data:
    cursor.execute("INSERT INTO wiki_data (title, url, content) VALUES (?, ?, ?)",
                   (entry["title"], entry["url"], entry["content"]))

# Commit changes and close connection
conn.commit()
conn.close()

print(f"✅ Data saved to {db_name} (SQLite Database)")
