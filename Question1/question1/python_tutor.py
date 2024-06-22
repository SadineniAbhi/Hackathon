import streamlit as st
import google.generativeai as genai
import sys
from io import StringIO
import re

# Set your Gemini API key here
GEMINI_API_KEY = "AIzaSyDWqS39CICihIZnsrwzGnKemF3pqa9sWeU"
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([
            "You are a helpful AI tutor for Python programming.",
            "When asked a theoretical you provide a detailed theory and when asked for code you give only the code.",
            "When unclear you provide both theory and code",
            "When you provide me with example code you always provide perfectly runnable code.",
            "Right now what i need from you is :",
            prompt
        ])
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def run_python_code(code):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    try:
        exec(code)
        sys.stdout = old_stdout
        return redirected_output.getvalue()
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {str(e)}"

def extract_code_blocks(text):
    pattern = r'```(?:python)?\s*([\s\S]*?)\s*```'
    return re.findall(pattern, text)

st.title("AI Python Tutor")

# Initialize session state
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = ""
if 'code_blocks' not in st.session_state:
    st.session_state.code_blocks = []

question = st.text_area("Enter your Python question or code:")
submit_button = st.button("Submit")

if submit_button and question:
    st.session_state.ai_response = get_ai_response(question)
    st.session_state.code_blocks = extract_code_blocks(st.session_state.ai_response)

if st.session_state.ai_response:
    st.markdown("### AI Tutor Response:")
    st.write(st.session_state.ai_response)

    for i, code in enumerate(st.session_state.code_blocks):
        st.markdown(f"### Code Block {i+1}:")
        st.code(code, language="python")
        if st.button(f"Run Code Block {i+1}", key=f"run_block_{i}"):
            output = run_python_code(code)
            st.markdown(f"### Output of Code Block {i+1}:")
            st.code(output)

st.markdown("---")
st.markdown("### Run Your Own Python Code")
user_code = st.text_area("Enter Python code to run:")
run_button = st.button("Run")

if run_button and user_code:
    output = run_python_code(user_code)
    st.markdown("### Output:")
    st.code(output)
