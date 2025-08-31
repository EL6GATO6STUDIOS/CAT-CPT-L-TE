import streamlit as st
from googletrans import Translator
from web import search

# Başlık
st.set_page_config(page_title="Cat CPT Lite", layout="wide")
st.title("🐱 Cat CPT Lite")

# Translator (otomatik Türkçe-İngilizce çeviri)
translator = Translator()

# Mesaj geçmişi
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Kullanıcı giriş kutusu
user_input = st.chat_input("Bir şey yaz...")

# Fonksiyon: günlük mü soru mu?
def is_question(text: str) -> bool:
    return "?" in text or any(word in text.lower() for word in ["ara", "nedir", "kimdir", "ne zaman", "nasıl", "kaç", "hangi"])

# Mesajları göster
for role, msg in st.session_state["messages"]:
    with st.chat_message(role):
        st.markdown(msg)

if user_input:
    # Kullanıcı mesajı göster
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state["messages"].append(("user", user_input))

    # Analiz
    if is_question(user_input):
        with st.chat_message("assistant"):
            st.markdown("🔎 Araştırıyorum...")

        # İngilizceye çevir
        translated_q = translator.translate(user_input, src="tr", dest="en").text

        # Web araması yap
        results = search(translated_q)
        if results:
            answer = f"🌍 İşte bulduklarım:\n\n"
            for r in results[:3]:
                # Türkçe'ye çevirerek yaz
                translated_title = translator.translate(r['title'], src="en", dest="tr").text
                translated_snippet = translator.translate(r['snippet'], src="en", dest="tr").text
                answer += f"- **{translated_title}**: {translated_snippet}\n\n[{r['link']}]({r['link']})\n\n"
        else:
            answer = "❌ Hiç sonuç bulamadım."

        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state["messages"].append(("assistant", answer))

    else:
        # Günlük cevap ver
        reply = f"😺 Güzel söyledin! '{user_input}' hakkında sohbet edebiliriz."
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state["messages"].append(("assistant", reply))
