import asyncio
import json
import os
from dotenv import load_dotenv
from urllib.parse import urldefrag
from crawl4ai import (AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode,
    MemoryAdaptiveDispatcher, LLMConfig)
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, JsonXPathExtractionStrategy
from src.ingestion.crawlers.crawler_examples import crawl_single_page
from src.ingestion.models.models import Restaurant

sample_html = """
"""

# css_schema = JsonCssExtractionStrategy.generate_schema(
#     sample_html,
#     schema_type=Restaurant.model_json_schema(),
#     llm_config=LLMConfig(
#         provider="openai/gpt-4o-mini",
#         api_token=os.getenv("OPENAI_API_KEY"),
#     )
# )

async def extract_restaurant_data(url:str) -> dict:
    """
    Schema to fetch the elements from the page:
    """
    schema = {
        "name": "Restaurant Listings",
        "baseSelector": ".XIWnB.z.y",
        "fields": [
            {
            "name": "restaurant_name",
            "selector": "div.fiohW",
            "type": "text"
            },
            {
            "name": "rating",
            "selector": "[data-automation='bubbleRatingValue'] span",
            "type": "text"
            },
            {
            "name": "cuisine_type",
            "selector": "span.biGQs._P.pZUbB.hmDzD",
            "type": "text"
            },
            {
            "name": "restaurant_url",
            "selector": "a.BMQDV",
            "type": "attribute",
            "attribute": "href"
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
        'restaurant_name': '1. O Buraco', 
        'rating': '4.2', 
        'cuisine_type': 'Mediterranean, European', 
        'restaurant_url': '/Restaurant_Review-g189180-d2419164-Reviews-O_Buraco-Porto_Porto_District_Northern_Portugal.html'
    }
    """
    data_list = json.loads(result.extracted_content)
    print(data_list[0]['restaurant_url'])

    # Process each restaurant and add its details
    for i, data in enumerate(data_list):
        data_details = await extract_restaurant_details_data(data['restaurant_url'])
        data_list[i]['metadata'] = data_details

        data_review = await extract_restaurant_reviews(data['restaurant_url'])
        data_list[i]['reviews'] = data_review

    # Save the results to a JSON file
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "restaurant_data.json")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {output_file}")
    return data_list

async def extract_restaurant_details_data(url:str):
    url_format = "https://www.tripadvisor.com" + url
    browser_config = BrowserConfig(browser_type="chromium", headless=True)

    schema_desc = {
    "name": "Restaurant Complete Info",
    "baseSelector": "body",
        "fields": [
        {
        "name": "restaurant_name",
        "selector": "h1.hzzSG",
        "type": "text"
        },
        {
        "name": "rating",
        "selector": "div[data-automation='bubbleRatingValue']",
        "type": "text"
        },
        {
        "name": "review_count",
        "selector": "[data-automation='bubbleReviewCount']",
        "type": "text"
        },
        {
        "name": "ranking",
        "selector": "span.diZaT",
        "type": "text"
        },
        {
        "name": "price_range",
        "selector": "span.cPbcf > span.bTeln:last-of-type a",
        "type": "text"
        },
        {
        "name": "review_summary",
        "selector": "div.aaQZA div.IGaaH",
        "type": "text"
        },
        {
            "name": "ai_highlights",
            "selector": "div.OykfZ div.CUmiT",
            "type": "nested_list",
            "fields": [
                {
                    "name": "category",
                    "selector": "span.ZNjnF",
                    "type": "text"
                },
                {
                    "name": "value",
                    "selector": "span.ezezH",
                    "type": "text"
                }
            ]
        },
        {
        "name": "schedule",
        "selector": "div[data-automation='hours-section'] div.f.e.Q3 > div.f",
        "type": "nested_list",
        "fields": [
            {
            "name": "day",
            "selector": "div.cGgaa",
            "type": "text"
            },
            {
            "name": "times",
            "selector": "div.cGgaa + div",
            "type": "text"
            }
        ]
        },
        {
        "name": "address",
        "selector": "span[data-automation='restaurantsMapLinkOnName']",
        "type": "text"
        },
        {
        "name": "website",
        "selector": "a[data-automation='restaurantsWebsiteButton']",
        "type": "attribute",
        "attribute": "href"
        },
        {
        "name": "detailed_cuisines",
        "selector": ".qXeDC .iPiKu:nth-child(1) .AWdfh",
        "type": "text"
        },
        {
            "name": "meal_types",
            "selector": ".qXeDC .iPiKu:nth-child(2) .AWdfh",
            "type": "text"
        },
        {
            "name": "special_diets",
            "selector": ".qXeDC .iPiKu:nth-child(3) .AWdfh",
            "type": "text"
        },
        ]   
    }

    strategy = JsonCssExtractionStrategy(schema=schema_desc, verbose=True)

    config = CrawlerRunConfig(
        extraction_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=url_format,
            config=config
        )   

    if not result.success:
        print(f"Error crawling {url}: {result.error_message}")
        return None
    
    # Debug print after success check
    if "Jump to all reviews" in result.extracted_content:
        result.extracted_content = result.extracted_content.replace("Jump to all reviews", "")

    print("Markdown result:", result.extracted_content)
    
    data = json.loads(result.extracted_content)
    return data

async def extract_restaurant_reviews(url: str):
    url_format = "https://www.tripadvisor.com" + url
    """
    Extracts user reviews from a Tripadvisor page using a robust JavaScript
    function that waits for the loading progress bar to disappear and reviews
    to be present.
    """
    schema_desc = {
      "name": "Restaurant Complete Info",
      "baseSelector": "div[data-automation='reviewCard']",
      "fields": [
        { 
            "name": "review_text", 
            "selector": "span.JguWG", 
            "type": "text" 
        }
      ]
    }

    strategy = JsonCssExtractionStrategy(schema=schema_desc)

    # This JS function waits for the progress bar (div.TSoOh) to be removed
    # AND for at least 5 review cards to be loaded. This is the most reliable method.
    wait_for_reviews_and_no_bar = """
    () => {
        const progressBar = document.querySelector("div.TSoOh");
        return !progressBar;
    }
    """

    config = CrawlerRunConfig(
        extraction_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
        wait_for=f"js:{wait_for_reviews_and_no_bar}"
    )

    browser_config = BrowserConfig(browser_type="chromium", headless=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url_format, config=config)

    if not result.success:
        print(f"Error crawling {url_format}: {result.error_message}")
        return None

    data = json.loads(result.extracted_content)
    print(json.dumps(data, indent=2))
    return data

