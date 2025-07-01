import asyncio
import json
import os
from dotenv import load_dotenv
from urllib.parse import urldefrag
from crawl4ai import (AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode,
    MemoryAdaptiveDispatcher, LLMConfig)
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, JsonXPathExtractionStrategy
from src.ingestion.crawler.crawler_examples import crawl_single_page
from src.ingestion.models.models import Restaurant

sample_html = """
<div class="vkMWZ _T Fl y">
    <div class="XIWnB z y">
        <div class="IcVzi y _T">
            <div class="vwOkl">
                <div>
                    <div class="mfKvs f e">
                        <div class="UIwAG f k">
                            <div class="KBZbF f e">
                                <div class="ZvrsW N G">
                                    <div class="AeLpB f K _T">
                                        <div class="PkmeC QA Pb PP Po PC R4">
                                            <img class="ktayA" src="https://static.tacdn.com/img2/restaurant-awards/Stars/1-Star.svg" alt="One MICHELIN Star">
                                            <span class="biGQs _P UFJyF Wf">MICHELIN</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="ZvrsW N G">
                                    <a href="/Restaurant_Review-g189180-d1656594-Reviews-Pedro_Lemos_Restaurante-Porto_Porto_District_Northern_Portugal.html" class="BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS">
                                        <div class="biGQs _P fiohW alXOW oCpZu GzNcM nvOhm UTQMg ZTpaU mtnKn ngXxk">29. Pedro Lemos Restaurante</div>
                                    </a>
                                    <div class="kzrsh">
                                        <div class="VVbkp">
                                            <div class="MyMKp u">
                                                <span aria-hidden="true">
                                                    <div class="biGQs _P pZUbB hmDzD" data-automation="bubbleRatingValue">
                                                        <span>4.5</span>
                                                    </div>
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <div class="ZvrsW N G">
                            <div class="ZvrsW N G biqBm">
                                <span class="f">
                                    <svg viewBox="0 0 24 24" width="16px" height="16px" class="d Vb egaXP UmNoP" aria-hidden="true">
                                        <path fill-rule="evenodd" clip-rule="evenodd" d="M14.051 6.549v.003l1.134 1.14 3.241-3.25.003-.002 1.134 1.136-3.243 3.252 1.134 1.14a1 1 0 0 0 .09-.008c.293-.05.573-.324.72-.474l.005-.006 2.596-2.603L22 8.016l-2.597 2.604a3.73 3.73 0 0 1-1.982 1.015 4.3 4.3 0 0 1-3.162-.657l-.023-.016-.026-.018-1.366 1.407 8.509 8.512L20.219 22l-.002-.002-6.654-6.663-2.597 2.76-7.3-7.315C1.967 8.948 1.531 6.274 2.524 4.198c.241-.504.566-.973.978-1.386l8.154 8.416 1.418-1.423-.039-.045c-.858-1.002-1.048-2.368-.62-3.595a4.15 4.15 0 0 1 .983-1.561L16 2l1.135 1.138-2.598 2.602-.047.045c-.16.151-.394.374-.433.678zM3.809 5.523c-.362 1.319-.037 2.905 1.06 4.103L10.93 15.7l1.408-1.496zM2.205 20.697 3.34 21.84l4.543-4.552-1.135-1.143z"></path>
                                    </svg>
                                    <span class="biGQs _P pZUbB hmDzD">Mediterranean, European</span>
                                </span>
                                <span class="biGQs _P pZUbB hmDzD">$$$$</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
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
    data = json.loads(result.extracted_content)
    data_details = await extract_restaurant_details_data(data[0]['restaurant_url'])
    print("Initial data -> ", data[0])
    print("Initial data descritpion -> ", data_details)


async def extract_restaurant_details_data(url:str):
    url_format = "https://www.tripadvisor.com/Restaurant_Review-g189180-d26193740-Reviews-Taberna_dos_Fernandes-Porto_Porto_District_Northern_Portugal.html"


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
        "name": "cuisine_types",
        "selector": "span.cPbcf > span.bTeln:not(:last-of-type) a",
        "type": "list"
        },
        {
        "name": "price_range",
        "selector": "span.cPbcf > span.bTeln:last-of-type a",
        "type": "text"
        },
        {
        "name": "features",
        "selector": "div.BrqJv div.sxnyJ",
        "type": "list"
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
            "name": "user_reviews",
            "selector": "div[data-automation='reviewCard']",
            "type": "nested_list",
            "fields": [
                {
                    "name": "author_name",
                    "selector": "a.ukgoS",
                    "type": "text"
                },
                {
                    "name": "author_info",
                    "selector": "div.vYLts",
                    "type": "text"
                },
                {
                    "name": "rating",
                    "selector": "svg[data-automation='bubbleRatingImage'] title",
                    "type": "text"
                },
                {
                    "name": "title",
                    "selector": "div[data-test-target='review-title'] a",
                    "type": "text"
                },
                {
                    "name": "date_of_visit",
                    "selector": "div.IlciT",
                    "type": "text"
                },
                {
                    "name": "review_text",
                    "selector": "span.JguWG",
                    "type": "text"
                }
            ]
        }
    ]
    }

    strategy = JsonCssExtractionStrategy(schema=schema_desc, verbose=True)

    config = CrawlerRunConfig(
        extraction_strategy=strategy,
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler() as crawler:
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

