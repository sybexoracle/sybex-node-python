from rich.console import Console
from src.aggregator.newsapi import NewsAPIAggregator

console = Console()
news = NewsAPIAggregator()
news_data = news.search("blockchain technology", language="en", page_size=5)

console.print_json(data=news_data)