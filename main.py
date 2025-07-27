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
from src.ingestion.processing.process import process_restaurant_data


async def main():
    """Main function to run the crawler."""
    load_dotenv()
    url_restaurants = "https://www.tripadvisor.com/Restaurants-g189180-Porto_Porto_District_Northern_Portugal.html"
    url_landmarks = "https://www.tripadvisor.com/Attractions-g189180-Activities-a_allAttractions.true-Porto_Porto_District_Northern_Portugal.html"
    url_activities = "https://www.tripadvisor.com/Attractions-g189180-Activities-c61-Porto_Porto_District_Northern_Portugal.html"
    url_tours = "https://www.tripadvisor.com/Attractions-g189180-Activities-c42-Porto_Porto_District_Northern_Portugal.html"
    url_concerts = "https://www.tripadvisor.com/Attractions-g189180-Activities-c58-Porto_Porto_District_Northern_Portugal.html"
    data = await extract_activity_data(url_concerts)
    # process_restaurant_data(data)
   

if __name__ == "__main__":
    asyncio.run(main()) 