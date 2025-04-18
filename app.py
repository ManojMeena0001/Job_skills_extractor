import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from io import StringIO
import PyPDF2
import io
import docx

from preprocessing import preprocess_text
from skill_extractor import extract_skills
from skill_categorizer import categorize_skills
from utils import get_file_text

# Set page configuration
st.set_page_config(
    page_title="JD Skill Extractor",
    page_icon="📝",
    layout="wide"
)

# App title
st.title("Job Description Skill Extractor")
st.markdown("""
This app helps you identify key technical skills and requirements from job descriptions. 
Simply paste your job description or upload a file below to get started.
""")

# Initialize session state variables if they don't exist
if 'extracted_skills' not in st.session_state:
    st.session_state.extracted_skills = None
if 'categorized_skills' not in st.session_state:
    st.session_state.categorized_skills = None
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = ""

# Input section
st.header("Job Description Input")
input_option = st.radio("Choose input method:", ["Paste text", "Upload file"])

if input_option == "Paste text":
    jd_text = st.text_area("Paste job description here:", 
                          height=300, 
                          placeholder="Copy and paste the job description text here...")
    
    if jd_text:
        st.session_state.jd_text = jd_text

else:  # Upload file option
    uploaded_file = st.file_uploader("Upload a job description file", 
                                    type=['txt', 'pdf', 'docx'])
    
    if uploaded_file is not None:
        try:
            jd_text = get_file_text(uploaded_file)
            st.session_state.jd_text = jd_text
            st.success(f"Successfully loaded file: {uploaded_file.name}")
            
            # Show a preview of the extracted text
            with st.expander("Preview extracted text"):
                st.write(jd_text[:500] + "..." if len(jd_text) > 500 else jd_text)
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Process button
if st.button("Extract Skills") and st.session_state.jd_text:
    with st.spinner("Analyzing job description..."):
        # Preprocess the text
        processed_text = preprocess_text(st.session_state.jd_text)
        
        # Extract skills
        extracted_skills = extract_skills(processed_text)
        st.session_state.extracted_skills = extracted_skills
        
        # Categorize skills
        categorized_skills = categorize_skills(extracted_skills)
        st.session_state.categorized_skills = categorized_skills

# Results display
if st.session_state.extracted_skills and st.session_state.categorized_skills:
    st.header("Results")
    
    # Display skills by category
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Extracted Skills by Category")
        
        for category, skills in st.session_state.categorized_skills.items():
            if skills:  # Only show categories with at least one skill
                st.markdown(f"**{category}**")
                
                # Display skills as chips/badges
                html_skills = ""
                for skill in skills:
                    # Create a styled badge for each skill
                    html_skills += f"""
                    <span style="display: inline-block; 
                                 background-color: rgba(0, 119, 181, 0.1); 
                                 border: 1px solid #0077B5; 
                                 border-radius: 16px; 
                                 padding: 4px 12px; 
                                 margin: 4px; 
                                 font-size: 14px;
                                 color: #0077B5;">
                        {skill}
                    </span>
                    """
                st.markdown(html_skills, unsafe_allow_html=True)
                st.markdown("---")
    
    with col2:
        st.subheader("Skill Distribution")
        
        # Prepare data for chart
        categories = []
        skill_counts = []
        
        for category, skills in st.session_state.categorized_skills.items():
            if skills:  # Only include categories with at least one skill
                categories.append(category)
                skill_counts.append(len(skills))
        
        chart_data = pd.DataFrame({
            'Category': categories,
            'Count': skill_counts
        })
        
        # Create bar chart using Plotly
        if not chart_data.empty:
            fig = px.bar(
                chart_data, 
                x='Category', 
                y='Count',
                title='Skills by Category',
                color='Count',
                color_continuous_scale=['#86888A', '#00A0DC', '#0077B5'],
                labels={'Count': 'Number of Skills', 'Category': 'Skill Category'}
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
                yaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data to generate visualization.")
    
    # All extracted skills
    with st.expander("View All Extracted Skills (Alphabetical)"):
        if st.session_state.extracted_skills:
            all_skills = sorted(st.session_state.extracted_skills)
            
            # Display as chips
            html_all_skills = ""
            for skill in all_skills:
                html_all_skills += f"""
                <span style="display: inline-block; 
                             background-color: rgba(0, 160, 220, 0.1); 
                             border: 1px solid #00A0DC; 
                             border-radius: 16px; 
                             padding: 4px 12px; 
                             margin: 4px; 
                             font-size: 14px;
                             color: #00A0DC;">
                    {skill}
                </span>
                """
            st.markdown(html_all_skills, unsafe_allow_html=True)
        else:
            st.info("No skills were extracted. Try another job description.")

# Information section at the bottom
with st.expander("About this app"):
    st.markdown("""
    ### JD Skill Extractor
    
    This application helps you extract and categorize technical skills from job descriptions. 
    
    #### How it works:
    1. Input a job description (paste text or upload a file)
    2. The app processes the text using NLP techniques
    3. Technical skills are extracted based on a comprehensive skill dictionary
    4. Skills are categorized into groups like Programming Languages, Tools, Cloud Platforms, etc.
    5. Results are displayed in an easy-to-read format
    
    #### Technologies used:
    - Streamlit for the web interface
    - spaCy for natural language processing
    - Fuzzy matching for skill detection
    - Plotly for data visualization
    """)
