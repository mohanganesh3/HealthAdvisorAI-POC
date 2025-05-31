import streamlit as st
from model_manager import ModelManager
from prompt_templates import PromptTemplates
from utils import validate_input, format_response, create_example_data, display_disclaimer
from config import APP_TITLE, APP_DESCRIPTION

# Configure Streamlit page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'model_manager' not in st.session_state:
    st.session_state.model_manager = ModelManager()
if 'model_ready' not in st.session_state:
    st.session_state.model_ready = False

def main():
    # Header
    st.title(APP_TITLE)
    st.markdown(f"*{APP_DESCRIPTION}*")
    
    # Display disclaimer
    display_disclaimer()
    
    # Sidebar for model management
    with st.sidebar:
        st.header("🤖 Model Management")
        
        # Model download and loading
        if not st.session_state.model_ready:
            if st.button("Download & Load Model", type="primary"):
                if st.session_state.model_manager.download_model():
                    if st.session_state.model_manager.load_model():
                        st.session_state.model_ready = True
                        st.rerun()
        else:
            st.success("✅ Model Ready!")
            
        st.divider()
        
        # Example data
        st.header("📋 Example Data")
        example_data = create_example_data()
        
        if st.button("Load Example Data"):
            st.session_state.example_symptoms = example_data["symptoms"]
            st.session_state.example_biomarkers = example_data["biomarkers"]
            st.session_state.example_remarks = example_data["remarks"]
            st.session_state.example_screen_time = example_data["screen_time"]
            st.session_state.example_health_tracking = example_data["health_tracking"]
            st.rerun()
    
    # Main content area
    if not st.session_state.model_ready:
        st.info("👆 Please download and load the model using the sidebar to get started.")
        return
    
    # Input form
    st.header("📝 Health Information Input")
    
    with st.form("health_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            symptoms = st.text_area(
                "Current Symptoms / Disease History:",
                value=st.session_state.get('example_symptoms', ''),
                height=100,
                placeholder="e.g., mild chest pain, shortness of breath, past asthma"
            )
            
            biomarkers = st.text_area(
                "Biomarkers (blood/lab values):",
                value=st.session_state.get('example_biomarkers', ''),
                height=100,
                placeholder="e.g., Hemoglobin: 13.5 g/dL, WBC Count: 7000 cells/µL"
            )
            
            remarks = st.text_area(
                "Additional Remarks:",
                value=st.session_state.get('example_remarks', ''),
                height=80,
                placeholder="Any additional observations or notes"
            )
        
        with col2:
            screen_time = st.text_area(
                "Screen Time Data:",
                value=st.session_state.get('example_screen_time', ''),
                height=100,
                placeholder="e.g., 9 hrs/day on Desktop, 6 hrs/day on Mobile"
            )
            
            health_tracking = st.text_area(
                "Health Tracking data:",
                value=st.session_state.get('example_health_tracking', ''),
                height=180,
                placeholder="Blood pressure, weight, steps, emotional state, etc."
            )
        
        submitted = st.form_submit_button("Get Health Recommendations", type="primary")
    
    # Generate recommendations
    if submitted:
        # Validate inputs
        inputs_to_validate = [
            (symptoms, "Symptoms/Disease History"),
            (biomarkers, "Biomarkers"),
            (health_tracking, "Health Tracking Data")
        ]
        
        validation_errors = []
        for input_text, field_name in inputs_to_validate:
            is_valid, error_msg = validate_input(input_text)
            if not is_valid:
                validation_errors.append(f"{field_name}: {error_msg}")
        
        if validation_errors:
            for error in validation_errors:
                st.error(error)
            return
        
        # Generate response
        try:
            with st.spinner("Analyzing your health data and generating recommendations..."):
                # Format user input
                formatted_input = PromptTemplates.format_user_input(
                    symptoms, biomarkers, remarks, screen_time, health_tracking
                )
                
                # Create prompt
                prompt = PromptTemplates.create_health_advisor_prompt(formatted_input)
                
                # Generate response
                response = st.session_state.model_manager.generate_response(prompt)
                
                # Format and display response
                formatted_response = format_response(response)
                
                st.header("🩺 Your Personalized Health Recommendations")
                st.write(formatted_response)
                
                # Option to download recommendations
                st.download_button(
                    label="📄 Download Recommendations",
                    data=formatted_response,
                    file_name="health_recommendations.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")

if __name__ == "__main__":
    main()