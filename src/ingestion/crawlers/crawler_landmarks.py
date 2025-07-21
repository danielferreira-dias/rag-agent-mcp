import json
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig, JsonCssExtractionStrategy


async def extract_landmark_data(url:str) -> dict:
    """
    Schema to fetch the elements from the page:
    """
    schema = {
        "name": "List of Attractions",
        "baseSelector": "article.GTuVU",
        "fields": [
            {
            "name": "title",
            "selector": "h3 .XfVdV",
            "type": "text"
            },
            {
            "name": "url",
            "selector": "a.BUupS",
            "type": "attribute",
            "attribute": "href"
            },
            {
            "name": "category",
            "selector": ".BKifx .alPVI > div:first-child",
            "type": "text"
            },
            {
            "name": "description",
            "selector": "[data-automation='listCardDescription']",
            "type": "text"
            },
            {
            "name": "rating",
            "selector": "[data-automation='bubbleRatingValue']",
            "type": "text"
            }
        ]
    }
    strategy = JsonCssExtractionStrategy(schema=schema, verbose=True)

    config = CrawlerRunConfig(
        extraction_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        result = await crawler.arun(
            url=url,
            config=config
        )   
    if not result.success:
        print(f"Error crawling {url}: {result.error_message}")
        return None
    
    
    """
    Data JSON schema:
    {
        'title': '1.Dom Luís I Bridge', 
        'url': '/Attraction_Review-g189180-d636456-Reviews-Dom_Luis_I_Bridge-Porto_Porto_District_Northern_Portugal.html', 
        'category': 'Bridges', 
        'rating': '4.6'
    }
    """
    data_list = json.loads(result.extracted_content)
    print(data_list)
    # print(data_list[0]['landmark_url'])

    return data_list