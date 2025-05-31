# HealthAdvisorAI-POC

A proof-of-concept health advisory system using LLaMA 3.2 1B model with optimized prompting for medical recommendations. Includes Streamlit demo interface for testing.

## What This Actually Does

This POC demonstrates how to build a functional health advisory system using a small, locally-running LLM. The core system takes user health data (symptoms, biomarkers, lifestyle metrics) and generates structured health recommendations using carefully crafted prompts. A Streamlit interface is provided for easy testing and demonstration.

## Technical Implementation

### Architecture
```
├── app.py                 # Streamlit demo interface
├── config.py             # Model and app configuration
├── model_manager.py      # Model download/loading/inference (CORE)
├── prompt_templates.py   # Prompt engineering templates (CORE)
├── utils.py              # Input validation and formatting
├── requirements.txt      # Dependencies
└── models/               # Downloaded model storage
```

### Core Components

**Model Management (`model_manager.py`)**
- Downloads LLaMA 3.2 1B Instruct (Q4_K_M quantized) from HuggingFace
- Uses `llama-cpp-python` for CPU inference
- Configuration: 4K context, temp=0.5, max_tokens=1000

**Prompt Engineering (`prompt_templates.py`)**
- Single comprehensive system prompt (not multiple tested templates)
- Structured to output 4 sections: Short-term risks, Long-term risks, Warnings, Advice
- Includes clinical reference ranges in the prompt
- Uses LLaMA chat format with proper tokens

**Frontend (`app.py`)**
- Streamlit demo interface for testing the POC
- Model download/load UI flow
- Basic input validation
- Response formatting and display

## Why This Model Choice

**LLaMA 3.2 1B Instruct** was chosen because:
- Small enough to run on consumer hardware (681MB quantized)
- Decent instruction following for its size
- Fast inference (~2-10 seconds depending on hardware)
- Good balance of capability vs. resource usage

The Q4_K_M quantization provides reasonable quality with significantly reduced memory footprint.

## Prompt Engineering Approach

The key technical insight is the structured prompt design:

1. **System Role Definition**: Explicit "AI Health Advisor" role with clinical reasoning instructions
2. **Output Format Specification**: Exact 4-section structure required
3. **Clinical Context**: Medical reference ranges embedded in prompt
4. **Response Rules**: Specific constraints (no bullet points, direct patient communication, data-grounded responses)
5. **Input Structure**: Formatted user data with clear categories

The prompt is approximately 2000 tokens and includes medical reference ranges to help the model reason about clinical values.

## Technical Specifications

**Model**: `hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF`
- Parameters: 1.2B
- Quantization: Q4_K_M (4-bit)
- File size: ~681MB
- Context window: 4096 tokens

**Runtime Configuration**:
```python
{
    "n_ctx": 4096,
    "n_threads": 4,
    "temperature": 0.5,
    "max_tokens": 1000,
    "top_p": 0.9,
    "repeat_penalty": 1.1,
}
```

**Dependencies**:
- `llama-cpp-python`: LLM inference engine (CORE)
- `huggingface-hub`: Model downloading (CORE)
- `streamlit`: Demo web interface
- Standard Python utilities

## Installation (Demo)

1. **Create virtual environment**:
   ```bash
   python -m venv health_advisor_env
   source health_advisor_env/bin/activate  # Linux/Mac
   # OR
   health_advisor_env\Scripts\activate     # Windows
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run demo**:
   ```bash
   streamlit run app.py
   ```

4. **First-time setup**:
   - Click "Download & Load Model" in sidebar
   - Wait for 681MB model download
   - Model loads into memory (~2GB RAM usage)
   - Enter health data and click "Get Health Recommendations"

## Input Data Structure

The system expects structured health data:
- **Symptoms/Disease History**: Text description of current symptoms and medical history
- **Biomarkers**: Lab values (blood work, vitals, etc.)
- **Clinical Notes**: Additional physician remarks or observations
- **Screen Time**: Digital device usage patterns
- **Health Tracking**: Steps, BP, sleep, emotional state, etc.

## Output Format

The model generates a structured response with:
1. **Short-Term Risks**: Immediate health concerns based on current data
2. **Long-Term Risks**: Chronic disease risk assessment
3. **Warnings**: Critical issues requiring medical attention
4. **Advice**: Personalized recommendations based on input data


## Performance Characteristics

**Response Time**: 5-30 seconds depending on hardware
**Memory Usage**: ~2GB RAM during inference
**Model Loading**: ~10-30 seconds initial load
**Accuracy**: Depends heavily on prompt quality and input data structure


## Development Notes

This is a **proof of concept** demonstrating:
- Local LLM deployment for healthcare applications
- Effective prompt engineering for domain-specific tasks  
- Model management for consumer hardware

**Demo Interface**: The Streamlit app (`app.py`) is purely for demonstration and testing purposes. The core POC consists of `model_manager.py` and `prompt_templates.py`, which can be integrated into any application architecture.

**Key Challenge**: The current 681MB model size presents deployment challenges for production servers. Organizations require smaller models (ideally <200MB) for cost-effective scaling and cloud deployment. This POC proves the concept works, but production deployment would need further model optimization or alternative approaches like:

- More aggressive quantization (Q2_K/Q3_K)
- Model pruning techniques
- Specialized smaller models trained specifically for health advisory
- API-based solutions for resource-constrained environments

The focus was on creating a working system that balances capability with practical deployment constraints.
