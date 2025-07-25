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
            "selector": ".mjDKG .alPVI .biGQs span",
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
        'title': '2.Sao Bento Railway Station', 
        'url': '/Attraction_Review-g189180-d2259445-Reviews-Sao_Bento_Railway_Station-Porto_Porto_District_Northern_Portugal.html', 
        'category': 'Rail Services • Architectural Buildings', 
        'description': 'Thetile workis amazing and I was lucky to have João from Touch Tours to be my guide as he was able to describe the...', 
        'rating': '4.5'
    }
    """
    data_list = json.loads(result.extracted_content)
    for i, data in enumerate(data_list):
        data_details = await extract_landmark_details(data['url'])
        data_list[i]['details'] = data_details
    
    print(data_list[2])

    return data_list

async def extract_landmark_details(url:str) -> dict:
    url_format = f"https://www.tripadvisor.com{url}"
    """
    Schema to fetch the elements from the page:
    """
    schema = {
    "name": "Landmark Review Snippets",
    "baseSelector": "body",
    "fields": [
        {
        "name": "review_snippets",
        "selector": "div.DXXIW._c",
        "type": "nested_list",
        "fields": [
            {
            "name": "rating",
            "selector": "svg[data-automation='bubbleRatingImage'] title",
            "type": "text"
            },
            {
            "name": "date",
            "selector": ".biGQs._P.pZUbB.navcl",
            "type": "text"
            },
            {
            "name": "title",
            "selector": ".biGQs._P.fiohW.ezezH",
            "type": "text"
            },
            {
            "name": "snippet_text",
            "selector": ".biGQs._P.pZUbB.alXOW",
            "type": "text"
            },
        ]
        },
        {
        "name": "highlited_reviews",
        "selector": "div[data-automation='reviewShelfCard']",
        "type": "list",
        "fields": [
            {
            "name": "rating",
            "selector": ".nKWJn.u title",
            "type": "text"
            },
            {
                "name": "review_text",
                "selector": "span.JguWG .biGQs._P.pZUbB.AWdfh",
                "type": "text"
            }
        ]
        },
        {
        "name": "nearby_locations",
        "selector": ".bVvJm .C",
        "type": "list",
        "fields": [
            {
            "name": "location_name",
            "selector": "div[data-automation='poiShelfAttractionCardTitle']",
            "type": "text"
            },
            {
            "name": "rating",
            "selector": "div[data-automation='bubbleRatingValue']",
            "type": "text"
            },
            {
            "name": "distance",
            "selector": "span.NnILp",
            "type": "text"
            }
        ]
        },
    ]
    }

    strategy = JsonCssExtractionStrategy(schema=schema, verbose=True)

    config = CrawlerRunConfig(
        extraction_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        result = await crawler.arun(
            url=url_format,
            config=config
        )   
    if not result.success:
        print(f"Error crawling {url_format}: {result.error_message}")
        return None
    
    print(json.loads(result.extracted_content))
    
    return json.loads(result.extracted_content)