import streamlit as st
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Cat CPT Lite", layout="centered")
st.title("Cat CPT Lite")  # Başlığı sadece Cat CPT Lite yaptık

# GPT2 text-generation pipeline
@st.cache_resource
def load_generator():
    return pipeline('text-generation', model='gpt2')

generator = load_generator()

# Cümle analiz fonksiyonu
def analyze_sentence(sentence):
    question_words = ["ne", "nasıl", "kim", "nerede", "hangi", "neden", "?"]
    research_part = ""
    chat_part = ""

    if any(word in sentence.lower() for word in question_words):
        research_part = sentence
        chat_part = sentence.replace(research_part, "")
    else:
        chat_part = sentence

    return chat_part.strip(), research_part.strip()

# Araştırma fonksiyonu
def research_answer(query):
    try:
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            if len(p.text) > 50:
                return p.text[:500] + "..."
        return "Araştırma sonucu bulunamadı."
    except:
        return "Araştırma sırasında bir hata oluştu."

# Sohbet fonksiyonu
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
