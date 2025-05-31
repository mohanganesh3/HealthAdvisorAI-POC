import os
import streamlit as st
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from config import MODEL_REPO, MODEL_FILENAME, MODEL_PATH, MODEL_CONFIG

class ModelManager:
    def __init__(self):
        self.model = None
        self.model_path = MODEL_PATH
        
    def download_model(self):
        """Download the model from Hugging Face Hub"""
        try:
            # Create models directory if it doesn't exist
            os.makedirs("models", exist_ok=True)
            
            if not os.path.exists(self.model_path):
                with st.spinner("Downloading model... This may take a few minutes."):
                    hf_hub_download(
                        repo_id=MODEL_REPO,
                        filename=MODEL_FILENAME,
                        local_dir="models",
                        local_dir_use_symlinks=False
                    )
                st.success("Model downloaded successfully!")
            return True
        except Exception as e:
            st.error(f"Error downloading model: {str(e)}")
            return False
    
    def load_model(self):
        """Load the model into memory"""
        try:
            if self.model is None:
                with st.spinner("Loading model..."):
                    self.model = Llama(
                        model_path=self.model_path,
                        n_ctx=MODEL_CONFIG["n_ctx"],
                        n_threads=MODEL_CONFIG["n_threads"],
                        verbose=False
                    )
                st.success("Model loaded successfully!")
            return True
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return False
    
    def generate_response(self, prompt):
        """Generate response using the loaded model"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            response = self.model(
                prompt,
                max_tokens=MODEL_CONFIG["max_tokens"],
                temperature=MODEL_CONFIG["temperature"],
                top_p=MODEL_CONFIG["top_p"],
                repeat_penalty=MODEL_CONFIG["repeat_penalty"],
                stop=["</s>", "<|end|>", "\n\nUser:", "\n\nHuman:"]
            )
            return response['choices'][0]['text'].strip()
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")