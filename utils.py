import streamlit as st
import re

def validate_input(text, min_length=50):
    """Validate user input"""
    if not text or len(text.strip()) < min_length:
        return False, f"Please provide at least {min_length} characters"
    return True, ""

def format_response(response):
    """Format the model response for readability"""
    response = response.strip()
    prefixes_to_remove = [
        "Based on the information provided,",
        "According to your health data,",
        "Here are my recommendations:",
        "I recommend the following:"
    ]
    for prefix in prefixes_to_remove:
        if response.lower().startswith(prefix.lower()):
            response = response[len(prefix):].strip()
    response = re.sub(r'\n\s*\n', '\n\n', response)
    return response

def create_example_data():
    """Create example data for users"""
    return {
        "full_input": """How are you feeling today? I have feel restless, because yesterday I was not exercised. 
Current Symptoms / Disease History: mild chest pain
Biomarkers (blood/lab values): Hemoglobin: 13.5 g/dL, WBC Count: 7000 cells/µL, Platelets: 250000/µL.
Remark: Patient experienced mild fatigue during the afternoon but recovered after hydration.
Screen Time data: 9 hrs/day on Desktop, 6 hrs/day on Mobile. Total: 9.7 hrs.
Health Tracking data: Blood Pressure: 120/80 mmHg, Diabetes (Fasting: 95 mg/dL, Post Meal: 135 mg/dL, Random: 110 mg/dL), Weight: 68 kg, gain weight, Emotional score: Relaxed (Score: 8), Note: Slept well, had a productive day, Steps per day: 7,850"""
    }

def display_disclaimer():
    """Display medical disclaimer"""
    st.warning("""
    ⚠️ **Medical Disclaimer**: This AI Health Advisor provides general wellness recommendations and should not replace professional medical advice. 
    Always consult with qualified healthcare professionals for medical concerns, diagnosis, or treatment decisions.
    """)