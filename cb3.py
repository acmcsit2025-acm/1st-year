from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

app = Flask(__name__)

# Limit CPU threads to prevent lagging
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
torch.set_num_threads(4)

# Path to the locally downloaded model
MODEL_PATH = "D:/8th sem project/TORN-GPT/gemma"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Load model in CPU-friendly mode
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float32,  # Use float32 for CPU
    low_cpu_mem_usage=True,     # Reduce RAM usage
    device_map={"": "cpu"}      # Force CPU execution
)

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")  # Ensure model runs on CPU
    output = model.generate(**inputs, max_length=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_response = generate_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
