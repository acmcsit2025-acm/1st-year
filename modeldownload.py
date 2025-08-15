from huggingface_hub import snapshot_download

model_name = "google/gemma-2b"
local_model_path = "C:\\Users\\USER\\OneDrive\\Desktop\\8th sem project\\TORN-GPT\\gemma"  # Change this to your preferred path

# Download and save the model
snapshot_download(repo_id=model_name, local_dir=local_model_path)
