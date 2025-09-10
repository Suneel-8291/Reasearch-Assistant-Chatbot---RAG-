import requests
from bs4 import BeautifulSoup

def load_url(url: str) -> str:
    """Fetch and clean text from a URL, spoofing User-Agent to bypass 403 errors."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove non-text elements
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = " ".join(soup.stripped_strings)
        return text

    except Exception as e:
        return f"Error loading {url}: {e}"

