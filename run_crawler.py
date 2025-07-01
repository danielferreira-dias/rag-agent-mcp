#!/usr/bin/env python3
"""
Script to run the crawler functions from the project root.
This avoids import issues by running from the correct directory.
"""

import asyncio
from dotenv import load_dotenv
from src.ingestion.crawlers.crawler_restaurants import extract_restaurant_data, extract_restaurant_details_data, extract_restaurant_reviews
from src.ingestion.crawlers.crawler_examples import crawl_single_page
from src.ingestion.processing.process import process_restaurant_data


async def main():
    """Main function to run the crawler."""
    load_dotenv()
    url = "https://www.tripadvisor.com/Restaurants-g189180-Porto_Porto_District_Northern_Portugal.html"
    data = await extract_restaurant_data(url)
    process_restaurant_data(data)
   

if __name__ == "__main__":
    asyncio.run(main()) 