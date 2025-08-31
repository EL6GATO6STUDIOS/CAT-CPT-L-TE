from bs4 import BeautifulSoup
import requests

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
        return "Araştırma sırasında bir hata oluştu."# utils.py
from bs4 import BeautifulSoup
import requests

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
