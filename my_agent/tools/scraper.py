import requests
from bs4 import BeautifulSoup


def smart_scraper(url: str) -> str:
    """
    Estrae il contenuto testuale pulito da un URL specificato.
    Utile per leggere articoli, documentazione o post di blog dopo averli trovati con la ricerca web.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        print(f"--- DEBUG SCRAPER: Status {response.status_code} per {url} ---")

        if response.status_code != 200:
            return f"Errore: Il sito ha risposto con status {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')

        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        text = soup.get_text(separator=' ')
        clean_text = ' '.join(text.split())

        if not clean_text:
            return "Errore: Pagina letta ma nessun testo estratto."

        return clean_text[:10000]
    except Exception as e:
        return f"Errore durante lo scraping: {str(e)}"