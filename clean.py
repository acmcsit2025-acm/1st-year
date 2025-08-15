import json
import re

# Load the JSON file
json_filename = "torn_wiki_data_cleaned.json"
with open(json_filename, "r", encoding="utf-8") as file:
    data = json.load(file)

# Function to clean the content
def clean_text(text):
    text = re.sub(r"\\n|\\t|\\", " ", text)  # Remove escape characters
    text = re.sub(r"https?://\S+", "", text)  # Remove URLs
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

# Process and clean all content
cleaned_data = []
for entry in data:
    if "content" in entry:
        entry["content"] = clean_text(entry["content"])
    cleaned_data.append(entry)

# Save the cleaned data back to JSON
cleaned_json_filename = "torn_wiki_data_final.json"
with open(cleaned_json_filename, "w", encoding="utf-8") as file:
    json.dump(cleaned_data, file, indent=4, ensure_ascii=False)

print(f"✅ Cleaned data saved as '{cleaned_json_filename}'")
