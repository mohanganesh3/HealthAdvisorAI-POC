# api_main.py
import time
import logging
from contextlib import asynccontextmanager # For the lifespan manager
from fastapi import FastAPI, HTTPException, Body, Request 

# Your existing modules (ensure these are in the same directory or accessible in PYTHONPATH)
# And ensure ModelManager uses logging, not Streamlit elements.
# And ensure PromptTemplates does not have duplicate <|begin_of_text|> if llama_cpp handles it.
from model_manager import ModelManager 
from prompt_templates import PromptTemplates
from utils import validate_input, format_response
# config.py is used by model_manager.py (MODEL_PATH, MODEL_CONFIG)

# Configure basic logging 
# This will show INFO level logs from your app and other libraries like uvicorn.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Logger for this specific file

# --- Pydantic Models (for request and response data validation) ---
from pydantic import BaseModel, Field

class HealthInput(BaseModel):
    user_input: str = Field(..., 
                            min_length=10, # Basic validation by Pydantic
                            description="All health information provided by the user.")

class HealthResponse(BaseModel):
    recommendations: str
    execution_time_seconds: float

# --- Lifespan Management for Model Loading ---
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """
    Manages the application's lifespan.
    Loads the model on startup and can handle cleanup on shutdown.
    """
    logger.info("Lifespan event: Startup - Attempting to load model...")
    
    # Initialize ModelManager and attempt to load the model.
    # The model_manager instance and its status will be stored in app.state.
    model_manager_instance = ModelManager() # Assumes ModelManager uses config.py for paths/params
    if model_manager_instance.load_model(): # load_model in ModelManager should use its own logger
        app_instance.state.model_manager = model_manager_instance
        app_instance.state.model_loaded_successfully = True
        logger.info("Lifespan event: Startup - Model loaded successfully and attached to app.state.")
    else:
        app_instance.state.model_manager = None 
        app_instance.state.model_loaded_successfully = False
        logger.error("Lifespan event: Startup - Model loading failed. Check ModelManager's logs for details.")
    
    yield  # The application runs while the yield is active

    # --- Shutdown logic (optional cleanup) ---
    logger.info("Lifespan event: Shutdown - Cleaning up resources if any...")
    current_model_manager = getattr(app_instance.state, 'model_manager', None)
    if current_model_manager:
        # If your ModelManager had a specific cleanup method (e.g., to release GPU memory explicitly),
        # you would call it here: e.g., current_model_manager.cleanup()
        logger.info("Lifespan event: Shutdown - Model resources (if any specific cleanup was needed) handled.")
    
    app_instance.state.model_manager = None
    app_instance.state.model_loaded_successfully = False
    logger.info("Lifespan event: Shutdown - Application state cleared.")


# --- FastAPI App Initialization with Lifespan ---
app = FastAPI(
    title="AI Health Advisor API",
    description="Provides health recommendations based on user input via a simple HTTP call.",
    version="1.1.0", # Increment version
    lifespan=lifespan # Assign the lifespan context manager
)

# --- API Endpoint ---
@app.post("/get_health_recommendations", response_model=HealthResponse)
async def get_health_recommendations_endpoint(
    request: Request, # Inject the Request object to access app.state
    payload: HealthInput = Body(...) # Use the Pydantic model for the request body
):
    """
    Accepts user health information string (input parameter) and returns 
    personalized health recommendations (response back).
    This endpoint functions like a programmatic interface (e.g., similar to calling an API like ChatGPT).
    """
    logger.info(f"Received request for /get_health_recommendations with input length: {len(payload.user_input)}")

    # Access model status and instance from app.state
    model_is_loaded = getattr(request.app.state, 'model_loaded_successfully', False)
    current_model_manager = getattr(request.app.state, 'model_manager', None)

    if not model_is_loaded or not current_model_manager:
        logger.warning("/get_health_recommendations: Attempted access when model not ready.")
        raise HTTPException(status_code=503, detail="Service Unavailable: Model is not loaded or failed to load. Please try again later.")

    user_text = payload.user_input

    # 1. Validate Input (using your existing util)
    # Pydantic already did a min_length check. Your custom util might have more complex rules.
    is_valid, error_msg = validate_input(user_text, min_length=50) # Using 50 from your original app.py
    if not is_valid:
        logger.warning(f"/get_health_recommendations: Invalid input - {error_msg}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {error_msg}")

    try:
        start_time = time.time()

        # 2. Format input and Create Prompt (using your existing PromptTemplates)
        formatted_input_for_prompt = PromptTemplates.format_user_input(user_text)
        prompt_text = PromptTemplates.create_health_advisor_prompt(formatted_input_for_prompt)
        logger.debug(f"Generated prompt for model (first 100 chars): {prompt_text[:100]}...")
        
        # 3. Generate Response (using the model_manager from app.state)
        raw_response = current_model_manager.generate_response(prompt_text)
        
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"/get_health_recommendations: Response generated in {execution_time:.2f} seconds.")

        # 4. Format Response (using your existing util)
        final_response = format_response(raw_response)
        logger.debug(f"Formatted response (first 100 chars): {final_response[:100]}...")

        return HealthResponse(
            recommendations=final_response,
            execution_time_seconds=round(execution_time, 2)
        )
    except ValueError as ve: 
        logger.error(f"ValueError during processing in /get_health_recommendations: {str(ve)}", exc_info=True)
        raise HTTPException(status_code=503, detail=f"Processing error: {str(ve)}") 
    except Exception as e:
        logger.error(f"Generic error in /get_health_recommendations: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred while generating recommendations.")

# --- Health Check Endpoint (Good Practice) ---
@app.get("/health")
async def health_check(request: Request): 
    """
    Checks if the API is running and the model is loaded.
    """
    model_is_loaded = getattr(request.app.state, 'model_loaded_successfully', False)
    
    if model_is_loaded:
        logger.info("/health: Health check successful, model is loaded.")
        return {"status": "ok", "message": "Model is loaded and API is healthy."}
    else:
        logger.warning("/health: Health check failed, model not loaded.")
        raise HTTPException(status_code=503, detail="Service Unavailable: Model not loaded or failed to load.")

# To run this (save as api_main.py):
# uvicorn api_main:app --reload --host 0.0.0.0 --port 8000