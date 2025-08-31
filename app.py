import streamlit as st
from transformers import pipeline
from utils import analyze_sentence, research_answer  # utils'ten alıyoruz

st.set_page_config(page_title="Cat CPT Lite", layout="centered")
st.title("Cat CPT Lite")

# GPT2 text-generation pipeline
@st.cache_resource
def load_generator():
    return pipeline('text-generation', model='gpt2')

generator = load_generator()

def chat_answer(chat_part):
    if not chat_part:
        return ""
    result = generator(chat_part, max_length=50, num_return_sequences=1)
    return result[0]['generated_text']

# Kullanıcı arayüzü
user_input = st.text_input("Bir şeyler yaz:")

if user_input:
    chat_part, research_part = analyze_sentence(user_input)
    
    response = ""
    
    if chat_part:
        response += "💬 Sohbet: " + chat_answer(chat_part) + "\n\n"
    if research_part:
        response += "🔎 Araştırma: " + research_answer(research_part)
    
    st.write(response)
