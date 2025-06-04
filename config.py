import os

# Model configuration
MODEL_REPO = "hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF"
MODEL_FILENAME = "llama-3.2-1b-instruct-q4_k_m.gguf"
MODEL_PATH = "/Users/mohanganesh/May30/health_advisor/models/llama-3.2-1b-instruct-q4_k_m.gguf"

# Optimized model parameters for speed
MODEL_CONFIG = {
    "n_ctx": 4096,  # Increased to handle large prompt
    "n_threads": 4,  # Match M1/M2 cores
    "n_batch": 512,
    "n_gpu_layers": -1,
    "temperature": 0.1,  # Deterministic output
    "max_tokens": 400,  # Reduced for speed
    "top_p": 0.85,  # Faster sampling
    "repeat_penalty": 1.1,
}

# App configuration
APP_TITLE = "AI Health Advisor"
APP_DESCRIPTION = "Get personalized health recommendations based on your health data"