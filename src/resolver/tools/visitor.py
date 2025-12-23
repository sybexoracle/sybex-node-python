import trafilatura
from langchain.tools import tool


@tool
def visit_news(url: str) -> str:
    """
    Simulates visiting a news article URL and returns a summary.

    Args:
        url (str): The URL of the news article to visit.
    Returns:
        str: A summary of the visited news article.
    """
    response = trafilatura.fetch_url(url)
    if response is None:
        return "Failed to retrieve the article."

    article_text = trafilatura.extract(response)
    if article_text is None:
        return "Failed to extract content from the article."

    return article_text
