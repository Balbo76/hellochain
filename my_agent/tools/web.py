from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

def web_search(query: str) -> str:
    """Cerca su internet informazioni aggiornate, documentazione o soluzioni a bug."""
    try:
        print(f"\033[94m[WEB] Ricerca in corso: {query}...\033[0m")
        return search.run(query)
    except Exception as e:
        return f"Errore durante la ricerca web: {str(e)}"