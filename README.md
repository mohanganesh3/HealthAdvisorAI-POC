
# HealthAdvisorAI-POC (FastAPI Backend API)

A proof-of-concept health advisory system using the LLaMA 3.2 1B model. This project provides a backend API built with FastAPI for generating medical recommendations based on user health data.

## What This Actually Does

This POC demonstrates how to build a functional health advisory backend using a small, locally-running LLM. The core system, exposed via an API:
* Accepts user health data (symptoms, biomarkers, lifestyle metrics) as a JSON input.
* Generates structured health recommendations using carefully crafted prompts and the LLaMA model.
* Provides an HTTP endpoint for programmatic interaction.

## Technical Implementation

### Architecture (FastAPI API)
Your project structure should reflect the FastAPI application:
```
├── api_main.py         # FastAPI application (CORE API logic)
├── config.py           # Model and app configuration
├── model_manager.py      # Model download/loading/inference (CORE)
├── prompt_templates.py   # Prompt engineering templates (CORE)
├── utils.py              # Input validation and formatting
├── requirements.txt      # Dependencies
└── models/               # Downloaded model storage (e.g., llama-3.2-1b-instruct-q4_k_m.gguf)
```

### Core Components

* **FastAPI Application (`api_main.py`)**:
    * Provides an HTTP POST endpoint (`/get_health_recommendations`) to receive health data and return recommendations.
    * Uses Pydantic for request and response data validation.
    * Integrates `ModelManager` for inference and `PromptTemplates` for prompt generation.
    * Loads the LLM on application startup using FastAPI's `lifespan` manager.
* **Model Management (`model_manager.py`)**:
    * Downloads LLaMA 3.2 1B Instruct (Q4_K_M quantized) from HuggingFace (if not present).
    * Uses `llama-cpp-python` for inference (supports CPU or GPU with Metal on macOS).
    * Configuration is managed in `config.py`.
* **Prompt Engineering (`prompt_templates.py`)**:
    * Contains the comprehensive system prompt designed for clinical advice.
    * Structures the output into multiple sections (e.g., risks, advice, recommendations).
    * Uses LLaMA 3 chat format with appropriate special tokens (ensure no duplicate BOS tokens).
* **Utilities (`utils.py`)**:
    * Handles input validation and response formatting.

## Model Configuration (Example from `config.py`)

Ensure your `config.py` contains your `MODEL_CONFIG`. Example:
```python
MODEL_CONFIG = {
    "n_ctx": 4096,
    "n_threads": 8,       # Adjust based on your CPU (e.g., 4 for M1/M2 performance cores)
    "n_gpu_layers": 20,   # Number of layers to offload to GPU (try -1 for all on M-series Mac)
    "temperature": 0.1,
    "max_tokens": 400,    # Max tokens for the generated response
    "top_p": 0.85,
    "repeat_penalty": 1.1,
    # "n_batch": 512, # If used
}
```

## Dependencies

Key dependencies (should be in `requirements.txt`):
* `fastapi`
* `uvicorn[standard]`
* `llama-cpp-python`
* `huggingface-hub`
* `pydantic`

## Installation and Running the API

1.  **Clone the repository (if applicable) and navigate to the project directory.**

2.  **Create and activate a virtual environment** (Recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate    # On Windows
    ```

3.  **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the API server**:
    ```bash
    uvicorn api_main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will be accessible at `http://localhost:8000`. The model will be downloaded (if not present in `./models`) and loaded on startup.

## Interacting with the API

* **Endpoint**: `POST /get_health_recommendations`
* **Request Body (JSON)**:
    ```json
    {
      "user_input": "Your detailed health information string here..."
    }
    ```
* **Response Body (JSON)**:
    ```json
    {
      "recommendations": "The generated health advice...",
      "execution_time_seconds": 12.34
    }
    ```
* **Interactive API Documentation (Swagger UI)**: Open your browser to `http://localhost:8000/docs`
* **Alternative API Documentation (ReDoc)**: Open your browser to `http://localhost:8000/redoc`

You can use tools like Postman, `curl`, or the interactive Swagger UI (recommended for easy testing) to send requests.

## Performance

* **Response Time**: Actively being optimized. Current times vary based on hardware and `MODEL_CONFIG` settings (especially `n_gpu_layers`, `max_tokens`, and `n_threads`).
* **Model Used**: `hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF` (~681MB)

## Development Notes

This is a proof-of-concept demonstrating a local LLM deployed as a backend API for health advisory. The core logic resides in `api_main.py`, `model_manager.py`, and `prompt_templates.py`.
