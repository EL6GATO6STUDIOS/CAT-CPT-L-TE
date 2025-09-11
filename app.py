import streamlit as st
from transformers import pipeline
import requests

# Basit Türkçe çeviri
from googletrans import Translator
translator = Translator()

# Hugging Face text generation modeli (özgün cümle için)
generator = pipeline("text-generation", model="gpt2")

# Araştırma yapma fonksiyonu
def search_web(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        res = requests.get(url).json()
        if "AbstractText" in res and res["AbstractText"]:
            return res["AbstractText"]
        elif "RelatedTopics" in res and len(res["RelatedTopics"]) > 0:
            return res["RelatedTopics"][0].get("Text", "Sonuç bulunamadı.")
        else:
            return "Herhangi bir sonuç bulamadım."
    except Exception as e:
        return f"Araştırma hatası: {e}"

# Streamlit UI
st.set_page_config(page_title="Cat CPT Lite", page_icon="🐱", layout="centered")
st.title("🐱 Cat CPT Lite")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sohbet alanı
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Bir şey yaz...")

if prompt:
    # Kullanıcı mesajı
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Araştırma mı, sohbet mi?
    if "araştır" in prompt.lower() or "nedir" in prompt.lower() or "kimdir" in prompt.lower():
        result = search_web(prompt)
        answer = generator(result, max_length=80, num_return_sequences=1)[0]['generated_text']
    else:
        answer = generator(prompt, max_length=60, num_return_sequences=1)[0]['generated_text']

    # Türkçe çeviri (model İngilizce ağırlıklı olduğu için)
    translated = translator.translate(answer, dest="tr").text

    with st.chat_message("assistant"):
        st.markdown(translated)

    st.session_state["messages"].append({"role": "assistant", "content": translated})
