import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Gemini API key from the environment
gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key is None:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

def create_story(prompt: str, age_group: str):
    age_group_prompts = {
        "Children": "Create a fun story of less than 1500 words about",
        "Teenagers": "Create an adventurous and engaging story of less than 1500 words about",
        "Young Adults": "Create an intriguing and captivating story which include some violence,action-scences of less than 1500 words about",
        "Adults": "Create a deep and thought-provoking which can include some violence,crime,horror story of less than 1500 words about"
    }
    age_group_prompt = age_group_prompts.get(age_group, "Create a store of less than 1500 words about")
    response = model.generate_content(
        f"{age_group_prompt} {prompt}"
    )
    return response.text

# Streamlit app
def main():
    st.title("Story Generator")

    # Get user input prompt and age group
    prompt = st.text_input("Enter the story prompt:")
    age_group = st.selectbox("Select the age group:", ["Children", "Teenagers", "Young Adults", "Adults"])

    if st.button("Generate Story"):
        if prompt:
            # Generate story based on the prompt and age group
            story = create_story(prompt, age_group)

            # Display the result
            st.header("**Generated Story:**")
            st.write(f"\n{story}")

            # Button to clear the response
            if st.button("Clear Response"):
                st.experimental_rerun()
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()
