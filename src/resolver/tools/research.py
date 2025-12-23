from langchain.tools import tool
from src.aggregator.newsapi import NewsAPIAggregator


@tool
def research_topic(topic: str) -> str:
    """
    Researches a given topic using the NewsAPI aggregator.

    Args:
        topic (str): The topic to research.

    Returns:
        str: A summary of the research findings.
    """
    aggregator = NewsAPIAggregator()
    data = aggregator.search(topic)

    articles = data.get("articles", [])
    if not articles:
        return "No articles found on this topic."

    summary = f"Found {len(articles)} articles on the topic '{topic}':\n"
    for article in articles[:5]:  # Limit to first 5 articles for brevity
        title = article.get("title", "No title")
        url = article.get("url", "No URL")
        summary += f"- {title}: {url}\n"

    return summary