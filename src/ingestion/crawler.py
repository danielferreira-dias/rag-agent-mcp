import asyncio
import os
from dotenv import load_dotenv
from urllib.parse import urldefrag
from crawl4ai import (AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode,
    MemoryAdaptiveDispatcher, LLMConfig)
from crawl4ai.extraction_strategy import LLMExtractionStrategy

async def crawl_single_page(url:str):
    """
    Asynchronously scrapes a single web page and prints its content in Markdown format.

    This function initializes an AsyncWebCrawler, runs it on the provided URL,
    and prints the resulting Markdown content to the console.

    Args:
        url (str): The URL of the web page to scrape.
    """
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        print(result.markdown)

async def crawl_recursive_batch(start_urls, max_depth=3, max_concurrent=10):
    """
    Recursively scrapes web pages in batches, starting from a list of initial URLs.

    This function performs a breadth-first crawl up to a specified maximum depth.
    It uses a memory-adaptive dispatcher to manage concurrent browser sessions
    and avoids re-visiting URLs.

    Args:
        start_urls (list[str]): A list of URLs to begin crawling from.
        max_depth (int, optional): The maximum recursion depth for the crawl. Defaults to 3.
        max_concurrent (int, optional): The maximum number of concurrent browser
                                     sessions. Defaults to 10.
    """
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=False
    )
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,      # Don't exceed 70% memory usage
        check_interval=1.0,                 # Check memory every second
        max_session_permit=max_concurrent   # Max parallel browser sessions
    )

    # Track visited URLs to prevent revisiting and infinite loops (ignoring fragments)
    visited = set()
    def normalize_url(url):
        # Remove fragment (part after #)
        return urldefrag(url)[0]
    current_urls = set([normalize_url(u) for u in start_urls])

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for depth in range(max_depth):
            print(f"\n=== Crawling Depth {depth+1} ===")
            # Only crawl URLs we haven't seen yet (ignoring fragments)
            urls_to_crawl = [normalize_url(url) for url in current_urls if normalize_url(url) not in visited]

            if not urls_to_crawl:
                break

            # Batch-crawl all URLs at this depth in parallel
            results = await crawler.arun_many(
                urls=urls_to_crawl,
                config=run_config,
                dispatcher=dispatcher
            )

            next_level_urls = set()

            for result in results:
                norm_url = normalize_url(result.url)
                visited.add(norm_url)  # Mark as visited (no fragment)
                if result.success:
                    print(f"[OK] {result.url} | Markdown: {len(result.markdown) if result.markdown else 0} chars")
                    # Collect all new internal links for the next depth
                    for link in result.links.get("internal", []):
                        next_url = normalize_url(link["href"])
                        if next_url not in visited:
                            next_level_urls.add(next_url)
                else:
                    print(f"[ERROR] {result.url}: {result.error_message}")
                    
            # Move to the next set of URLs for the next recursion depth
            current_urls = next_level_urls

async def extract_restaurants(url:str):
    ...
    

if __name__ == "__main__":
    load_dotenv()
    url = "https://www.google.com/search?q=porto+restaurants&client=firefox-b-d&sca_esv=86c72741684d2a2b&udm=1&sxsrf=AE3TifPt__DT1uW2DpU9qdB4Y6006XwiLw:1751223130198&ei=WothaL3yC9-pkdUPruCXyQ4&start=0&sa=N&sstk=Ac65TH7LbB8oei00wKy9xaZeVdwy6h6HgnvwFuvsZMA9zoli9a0iU7hYDiywJYjXK9ZhG8hl5IzmtDMUJm1h3p2G9XYPr6m1xk2cRagqZzvgvbEg9H0ei0rNCvFd_dkMc2p_&ved=2ahUKEwi9h-TEppeOAxXfVKQEHS7wJek4ChDx0wN6BAgJEAI&biw=2300&bih=1172&dpr=1.09"
    asyncio.run(crawl_single_page(url))
    # asyncio.run(crawl_recursive_batch([url], max_depth=3, max_concurrent=10))