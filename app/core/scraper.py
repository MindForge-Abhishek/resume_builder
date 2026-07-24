import httpx
from bs4 import BeautifulSoup

def scrape_company_info(url: str) -> dict:

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36  (KHTML, like Gecko) "
            "Chrome/120.0.0.0 safari/537.36"
        )
    }

    try :
        response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
        response.raise_for_status()

    except httpx.RequestError as e:
        return {"title": "", "text": "", "error": f"Could not reach {url}: {str(e)}"}

    except httpx.HHTPStatusError as e:
        return {"title": "", "text": "", "error": f"HTTP {e.response.status_code} from {url}"}

    soup = BeautifulSoup(response.text, "lxml")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title else "Unknown Company"

    raw_text = soup.get_text(separator =" ", strip =True)

    cleaned = " ".join(raw_text.split())

    trimmed = cleaned[:3000]

    return {
    "title": title,
    "text": trimmed,
    "error": None
}