from urllib.parse import urldefrag
from crawl4ai import (AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator, MemoryAdaptiveDispatcher)

async def crawl_single_page(url:str):
    """
    Asynchronously scrapes a single web page and prints its content in Markdown format.

    This function initializes an AsyncWebCrawler, runs it on the provided URL,
    and prints the resulting Markdown content to the console.

    Args:
        url (str): The URL of the web page to scrape.
    """
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,
            "escape_html": False,
            "body_width": 80
        }
    )

    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=config
        )


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