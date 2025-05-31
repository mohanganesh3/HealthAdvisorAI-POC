import os

# Model configuration
MODEL_REPO = "hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF"
MODEL_FILENAME = "llama-3.2-1b-instruct-q4_k_m.gguf"
MODEL_PATH = os.path.join("models", MODEL_FILENAME)

# Model parameters
MODEL_CONFIG = {
    "n_ctx": 4096,
    "n_threads": 4,
    "temperature": 0.5,
    "max_tokens": 1000,
    "top_p": 0.9,
    "repeat_penalty": 1.1,
}

# App configuration
APP_TITLE = "AI Health Advisor"
APP_DESCRIPTION = "Get personalized health recommendations based on your symptoms, biomarkers, and lifestyle data"