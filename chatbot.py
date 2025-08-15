import sqlite3
import openai
from flask import Flask, request, jsonify

# Initialize Flask App
app = Flask(__name__)

# Initialize OpenAI API Key
openai.api_key = "your-api-key"  # Replace with your actual API key

# Function to fetch relevant context from the database
def search_database(query):
    try:
        conn = sqlite3.connect("torn_wiki.db")
        cursor = conn.cursor()

        # Search for relevant content
        cursor.execute("SELECT content FROM wiki_data WHERE content LIKE ? LIMIT 5", ("%" + query + "%",))
        results = cursor.fetchall()
        conn.close()

        # Combine results into a single context string
        return " ".join(row[0] for row in results) if results else "No relevant data found."

    except sqlite3.Error as e:
        return f"Database Error: {str(e)}"

# Function to get chatbot response using OpenAI
def ask_gpt(user_query, context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Torn City game expert. Answer based on the context provided."},
                {"role": "user", "content": f"Context: {context}. Now answer this: {user_query}"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    
    except openai.error.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"

# API route for chatbot response
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        # Debugging: Print received data
        print("🔍 Debug: Received data ->", data)

        if not data or "query" not in data:
            return jsonify({"response": "Invalid input. Please send JSON data with a 'query' key."})

        user_query = data["query"].strip()

        if not user_query:
            return jsonify({"response": "Invalid input. Query cannot be empty."})

        # Fetch relevant context from database
        context = search_database(user_query)
        print("✅ Debug: Database context ->", context)

        # Generate response using OpenAI
        response = ask_gpt(user_query, context)
        print("✅ Debug: AI Response ->", response)

        return jsonify({"response": response})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"response": f"Internal Server Error: {str(e)}"})

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
