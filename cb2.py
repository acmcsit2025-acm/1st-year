from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Initialize Flask app
app = Flask(__name__)

# Model details
MODEL_NAME = "google/gemma-7b"

# Load tokenizer and model
print("Loading model... This may take a few minutes.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)
print("Model loaded successfully!")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"response": "Please enter a message!"})

    # Tokenize input
    inputs = tokenizer(user_input, return_tensors="pt").to("cuda")

    # Generate response
    with torch.no_grad():
        output = model.generate(**inputs, max_length=100)

    response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
