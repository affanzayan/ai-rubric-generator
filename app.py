import streamlit as st
from groq import Groq

# 1. Set up the page layout
st.set_page_config(page_title="AI Rubric Generator", page_icon="📝", layout="centered")

# 2. App Title and Description
st.title("📝 AI Project Rubric Generator")
st.write("Generate professional, customized grading rubrics in seconds. Powered by Groq (100% Free & Fast!)")

# 3. Sidebar for API Key (Keeps your key secure!)
st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
st.sidebar.info("Get a free key at console.groq.com. It is secure and only used for this session.")

# 4. User Inputs
st.subheader("Project Details")
topic = st.text_input("What is the project about?", placeholder="e.g., 8th Grade Science Fair on Renewable Energy")
grade_level = st.text_input("Grade Level", placeholder="e.g., 8th Grade")
num_criteria = st.slider("How many grading criteria?", 3, 6, 4)

# 5. The Magic Button
if st.button("✨ Generate Rubric", use_container_width=True):
    if not api_key:
        st.warning("Please enter your Groq API key in the left sidebar.")
    elif not topic:
        st.warning("Please enter a project topic!")
    else:
        with st.spinner("AI is writing your rubric (this will take ~1 second)..."):
            # Initialize the Groq client
            client = Groq(api_key=api_key)
            
            # Create the "Mega-Prompt" for the AI
            prompt = f"""
            Act as an expert {grade_level} teacher. 
            Create a comprehensive grading rubric for a project on: "{topic}".
            Include exactly {num_criteria} distinct grading criteria.
            Format the output strictly as a clean Markdown table with the following columns:
            Criteria | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1)
            """
            
            try:
                # Call the Groq API (using Llama 3 70B, which is free and incredibly fast)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                rubric_text = response.choices[0].message.content
                
                # Display the result
                st.success("Rubric generated successfully!")
                st.markdown(rubric_text)
                
                # Add a download button
                st.download_button("📥 Download Rubric as Text", rubric_text, file_name="rubric.txt")
                
            except Exception as e:
                st.error(f"An error occurred. Check your API key. Details: {e}")
