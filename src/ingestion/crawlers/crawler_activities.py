import json
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig, JsonCssExtractionStrategy

async def extract_activity_data(url:str) -> dict:
    """
    Schema to fetch the elements from the page:
    """
    schema = {
        "name": "tour_card_details",
        "baseSelector": "article.GTuVU",
        "fields": [
            {
            "name": "title",
            "selector": "div.XfVdV",
            "type": "text"
            },
            {
            "name": "url",
            "selector": "a.BUupS",
            "type": "attribute",
            "attribute": "href"
            },
            {
            "name": "tour_type",
            "selector": "div.dxkoL .alPVI > div:nth-child(1)",
            "type": "text"
            },
            {
            "name": "rating",
            "selector": "[data-automation='bubbleRatingValue']",
            "type": "text"
            },
            {
            "name": "description",
            "selector": "span.SwTtt",
            "type": "text"
            },
            {
            "name": "duration",
            "selector": "div.bRMrl",
            "type": "text"
            },
            {
            "name": "free_cancellation",
            "selector": "div.FUUWF .aTSjG span.biGQs",
            "type": "text"
            },
            {
            "name": "recommendation_rate",
            "selector": ".GvxaA span.biGQs",
            "type": "text"
            },
            {
            "name": "price",
            "selector": "div[data-automation='cardPrice']",
            "type": "text"
            },
            {
            "name": "price_unit",
            "selector": ".ZbAEz > div > div:nth-child(3)",
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
        "title": "30.Boat Trip to Régua Through the Douro Valley with Breakfast and Lunch",
        "tour_type": "Day Trips",
        "rating": "4.6",
        "description": "This is the cruise everyone talks about! Enjoy a sublime boat ride: embark in the city of Porto and enjoy the beauty of …",
        "duration": "6+ hours",
        "free_cancellation": "Free cancellation",
        "price": "$97",
        "price_unit": "per adult"
    }
    """
    data_list = json.loads(result.extracted_content)
    print(result.extracted_content)

    for i, data in enumerate(data_list):
        data_details = await extract_activity_details(data['url'])
        data_list[i]['details'] = data_details
    
    return data_list


async def extract_activity_details(url:str) -> dict:
    url_format = f"https://www.tripadvisor.com{url}"
    """
    Schema to fetch the elements from the page:
    """
    schema = {
    "name": "Activity Details",
    "baseSelector": "div.IsYTu",
    "fields": [
        {
        "name": "about",
        "selector": "section[id*='ProductAboveTheFoldInfo'] div[class*='fIrGe']",
        "type": "text",
        },
        {
        "name": "key_details",
        "selector": "div[data-automation='WebPresentation_ProductKeyDetailsSectionV2'] div.f.Q2._Y",
        "type": "nested_list",
        "fields": [
            {
            "name": "detail",
            "selector": "span.biGQs",
            "type": "text"
            },
        ]
        },
        {
        "name": "value_propositions",
        "selector": "div[data-automation='valuePropsSection'] div.mLcBS",
        "type": "nested_list",
        "fields": [
            {
            "name": "title",
            "selector": "button",
            "type": "text"
            },
            {
            "name": "description",
            "selector": "span.biGQs:last-child",
            "type": "text"
            },
        ]
        },
        {
        "name": "inclusions_exclusions_text",
        "selector": "dl",
        "type": "nested_list",
        "fields": [
            {
            "name": "full_inclusion_details",
            "selector": "dt:nth-of-type(1) + dd",
            "type": "text"
            },
        ]
        },
        {
        "name": "what_to_expect",
        "selector": ".tyUdl._d",
        "type": "text",
        },
        {
        "name": "whats_included",
        "selector": ".tyUdl ul.IMSns",
        "type": "text",
        },
        {
        "name": "additional_info",
        "selector": "dt:nth-of-type(4) + dd ul.IMSns li.seKux",
        "type": "nested_list",
        "fields": [
            {
            "name": "point",
            "selector": "span",
            "type": "text",
            },
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
    """
    {
        'about': 'This tour is more than a simple visit to Peneda-Gerês National Park: it’s a feeling!\nEmbrace your adventurous side outside the busy city of Oporto: experiencing beautiful 
        landscapes, magical paths, a waterfall, a lagoon, an typical village and a tasty local gastronomy all emerged in magnificent mountains.
        \n\nBegin your journey with a 4x4 pick-up at the our meeting points, joining a small group of like-minded adventurers. 
        Explore breathtaking mountain landscapes on short walks to a crystal-clear lagoon and a magical waterfall—perfect for grounding yourself in nature or enjoying a refreshing swim.
        \n\nStep back in time as we visit a typical village, where you’ll discover a fascinating way of life rooted in traditions and a commitment to heritage and cultural preservation.
        \n\nFood is a great way to preserve culture, and you’ll enjoy a traditional meal in a welcoming local restaurant, featuring fair, flavorful, and delicious food—green wine included!
        \n\n*Alternative plan for rainy days available!', 
        'key_details': [{'detail': 'Ages 3-75, max of 28 per group'}, {'detail': 'Duration: 9–10 hours'}, {'detail': 'Start time: Check availability'}, {'detail': 'Mobile ticket'}], 
        'value_propositions': [{'title': 'Free cancellation', 'description': 'Free cancellation'}, {'title': 'Reserve now & pay later', 'description': 'Reserve now & pay later'}, {'title': 'Lowest price guarantee', 'description': 'Lowest price guarantee'}], 
        'inclusions_exclusions_text': [{'full_inclusion_details': "Pick-up and drop-off at preselected meeting pointsSmall-group tour and routes adjusted to weather conditionsParticipative tourism: contribute to our reforestation projectInsurance;Lunch & wine in a local Restaurant.Friendly nature local guide4x4 Land Rover experienceWhat's not includedGratuitiesPersonal expenses"}], 
        'what_to_expect': 'ItineraryThis is a typical itinerary for this productStop At:Peneda-Geres National Park, Peneda-Geres National Park, Northern Portugal- Discover the Portuguese countryside surrounded by beautiful mountains\n\n- Immerse yourself in wild nature and swim in the crystal-clear waters of a waterfall and lagoon\n\n- Enjoy a traditional meal at a local restaurant and try green wine\n\n- Get to know a typical village and their ways of living\nParticipative tourism: be a part of our reforestation projectDuration: 7 hours', 
        'additional_info': 'Pick-up and drop-off at preselected meeting pointsSmall-group tour and routes adjusted to weather conditionsParticipative tourism: contribute to our reforestation projectInsurance;Lunch & wine in a local Restaurant.Friendly nature local guide4x4 Land Rover experience'
    }
    
    """
    return json.loads(result.extracted_content)