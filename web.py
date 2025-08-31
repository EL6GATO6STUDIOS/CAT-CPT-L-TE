import requests

def search(query, num_results=5):
    """
    Basit web arama fonksiyonu.
    Google yerine DuckDuckGo API üzerinden çalışır.
    """
    url = f"https://duckduckgo.com/html/?q={query}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    results = []
    if response.status_code == 200:
        text = response.text

        # Çok basit bir parse (daha sağlam istersen BeautifulSoup ekleyebiliriz)
        parts = text.split('<a rel="nofollow" class="result__a"')
        for p in parts[1:num_results+1]:
            try:
                link = p.split('href="')[1].split('"')[0]
                title = p.split('>')[1].split('<')[0]
                snippet = "..."  # DuckDuckGo snippet almak için ekstra parse gerekir
                results.append({
                    "title": title,
                    "link": link,
                    "snippet": snippet
                })
            except:
                continue
    return results
