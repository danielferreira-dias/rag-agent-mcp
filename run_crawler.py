#!/usr/bin/env python3
"""
Script to run the crawler functions from the project root.
This avoids import issues by running from the correct directory.
"""

import asyncio
from dotenv import load_dotenv
from src.ingestion.crawler import extract_restaurant_data
from src.ingestion.crawler_examples import crawl_single_page


async def main():
    """Main function to run the crawler."""
    load_dotenv()
    
    url = "https://www.tripadvisor.com/FindRestaurants?geo=189180&offset=0&sort=FEATURED&establishmentTypes=10591&broadened=false"
    # await crawl_single_page(url)
    await extract_restaurant_data(url)
    
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