#!/usr/bin/env python3
"""
Script to run the crawler functions from the project root.
This avoids import issues by running from the correct directory.
"""

import asyncio
from dotenv import load_dotenv
from src.ingestion.crawlers.crawler_activities import extract_activity_data
from src.ingestion.crawlers.crawler_landmarks import extract_landmark_data
from src.ingestion.crawlers.crawler_restaurants import extract_restaurant_data, extract_restaurant_details_data, extract_restaurant_reviews
from src.ingestion.crawlers.crawler_examples import crawl_single_page
from src.ingestion.crawlers.crawler_tourism import extract_tourism_data
from src.ingestion.processing.process import process_restaurant_data


async def main():
    """Main function to run the crawler."""
    load_dotenv()
    url_restaurants = "https://www.tripadvisor.com/Restaurants-g189180"
    url_landmarks = "https://www.tripadvisor.com/Attractions-g189180-Activities-a_allAttractions"
    url_activities = "https://www.tripadvisor.com/Attractions-g189180-Activities-c61"
    url_tours = "https://www.tripadvisor.com/Attractions-g189180-Activities-c42"
    url_concerts = "https://www.tripadvisor.com/Attractions-g189180-Activities-c58"
    url_tourism = "https://www.tripadvisor.ie/Tourism-g189180"
    data = await extract_tourism_data(url_tourism)
    # data = await extract_activity_data(url_concerts)
    # process_restaurant_data(data)
   

if __name__ == "__main__":
    asyncio.run(main()) 