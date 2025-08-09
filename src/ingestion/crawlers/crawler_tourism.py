from crawl4ai import (AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator, MemoryAdaptiveDispatcher, JsonCssExtractionStrategy)
import json
import os

async def extract_tourism_data(url:str) -> dict:
    """
    Schema to fetch the elements from the page:
    """
    schema = {
        "name": "Tourism Information",
        "baseSelector": "body",
        "fields": [
            {
            "name": "tourism_name",
            "selector": "div.TQENi.k._Y h1",
            "type": "text"
            },
            {
            "name": "tourism_description",
            "selector": "div.biGQs._P.pZUbB.AWdfh",
            "type": "text"
            },
            {
            "name": "travel_advice",
            "selector": "div.IDaDx.OJypB.Iwmxp.mvTrV.cyIij.fluiI.SMjpI",
            "type": "nested_list",
            "fields": [
                {
                    "name": "title",
                    "selector": "div.biGQs._P.fiohW.alXOW.EEXWj.GzNcM.BYtua.UTQMg.alvrA.KeZJf",
                    "type": "text"
                },
                {
                    "name": "subtitle",
                    "selector": "div.biGQs._P.fiohW.qWPrE.tyUdl.AWdfh",
                    "type": "text"
                },
            ]
            },
            {
            "name": "travel_advice_faq",
            "selector": "div.IDaDx.OJypB",
            "type": "nested_list",
            "fields": [
                {
                    "name": "title",
                    "selector": "h2.biGQs._P.fiohW.RnSgX",
                    "type": "text"
                },
                {
                    "name": "questions_and_answers",
                    "selector": "dl",
                    "type": "nested_list",
                    "fields": [
                        {
                            "name": "question",
                            "selector": "dt",
                            "type": "text"
                        },
                        {
                            "name": "question",
                            "selector": "dl",
                            "type": "text",
                            "fields": [
                                {
                                    "name": "question_title",
                                    "selector": "h4.biGQs._P.fiohW.roAGK.uPlAb.ezezH.",
                                    "type": "text"
                                },
                                {
                                    "name": "question_answer",
                                    "selector": "p.biGQs._P.fiohW.AWdfh",
                                    "type": "text"
                                }
                            ]
                        },
                    ]
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
            url=url,
            config=config
        )   
    if not result.success:
        print(f"Error crawling {url}: {result.error_message}")
        return None
    
    
    """
    Data JSON schema:
    {
        
    }
    """
    data_list = json.loads(result.extracted_content)
    print(data_list[0])

    return data_list
