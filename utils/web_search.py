import requests
from config.config import SERPER_API_KEY

def serper_search(query: str, num_results: int = 5):
    """Perform a web search using Serper API."""
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": num_results}

    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

        # Extract useful info
        results = []
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
        return results
    except Exception as e:
        return [{"title": "Error", "link": "", "snippet": str(e)}]
