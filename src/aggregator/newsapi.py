from requests import Session
from src.constants import NEWSAPI_API_KEY


class NewsAPIAggregator:
    def __init__(self) -> None:
        self.instance: Session = Session()
        self.instance.headers.update({"Authorization": NEWSAPI_API_KEY}) # type: ignore

    def search(self, query: str, language: str = "en", page_size: int = 10):
        all_articles = self.instance.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "language": language,
                "pageSize": page_size,
                "apiKey": NEWSAPI_API_KEY,
            },
        )
        return all_articles.json()
