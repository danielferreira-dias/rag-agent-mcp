#!/usr/bin/env python3
"""
Script to run the crawler functions from the project root.
This avoids import issues by running from the correct directory.
"""

import asyncio
from dotenv import load_dotenv
from src.ingestion.crawler.crawler import extract_restaurant_data, extract_restaurant_details_data, extract_reviews_data
from src.ingestion.crawler.crawler_examples import crawl_single_page
from src.ingestion.processing.process import process_restaurant_data


async def main():
    """Main function to run the crawler."""
    load_dotenv()
    
    url = "https://www.tripadvisor.com/FindRestaurants?geo=189180&offset=0&sort=FEATURED&establishmentTypes=10591&broadened=false"
    # await crawl_single_page(url)
    # data = await extract_restaurant_data(url)
    data = await extract_restaurant_details_data(url)
    # data_processed = process_restaurant_data(data)
    # print(data_processed[0].model_dump_json())
    
    # Uncomment the lines below to run other functions:
    # print("Running crawler with LLM extraction...")
    # await craw_page_with_llms(url)
    # 
    # print("Running single page crawl...")
    # await crawl_single_page(url)
    # 
    # print("Running recursive batch crawl...")
    # await crawl_recursive_batch([url], max_depth=3, max_concurrent=10)

if __name__ == "__main__":
    asyncio.run(main()) 