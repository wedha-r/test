import streamlit as st
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Function to generate story
def generate_english_story(title, theme, minutes=2):
    estimated_words = min(int(minutes) * 100, 500)  # Cap to 500 words
    instruction = (f"Write a children's {theme} story in English titled '{title}' "
                   f"in approximately {estimated_words} words.")
    data = {
        "contents": [{
            "parts": [{"text": instruction}]
        }]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "Sorry, I couldn't generate the story."
    return f"Error: {response.text}"

# Streamlit UI
st.title("Children's Story Generator")

title = st.text_input("Enter story title")
theme = st.selectbox("Choose story theme", options=["Adventure", "Anime", "Moral", "Fun", "Fantasy", "Science", "Mystery", "Friendship"])
minutes = st.number_input("Story length (minutes)", min_value=1, max_value=10, value=2)

if st.button("Generate Story"):
    if not title.strip():
        st.error("Please enter a story title.")
    else:
        with st.spinner("Generating story..."):
            story = generate_english_story(title, theme.lower(), minutes)
        if story.startswith("Error:") or story.startswith("Sorry"):
            st.error(story)
        else:
            st.subheader("Generated Story")
            st.write(story)
