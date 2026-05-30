import asyncio
import re
from urllib.parse import urljoin, urlparse

from apify import Actor
from crawlee import EnqueueStrategy
from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext

async def main() -> None:
    async with Actor:
        # Get input parameter dictionary
        actor_input = await Actor.get_input() or {}
        
        # Parse inputs
        start_urls_input = actor_input.get('startUrls', [])
        link_regex = actor_input.get('linkRegex', '.*')
        max_requests = actor_input.get('maxRequests', 50)
        max_depth = actor_input.get('maxDepth', 2)

        # Extract URLs from input format
        start_urls = []
        for item in start_urls_input:
            if isinstance(item, dict):
                url = item.get('url')
                if url:
                    start_urls.append(url)
            elif isinstance(item, str):
                start_urls.append(item)

        if not start_urls:
            Actor.log.error('No start URLs provided in the input.')
            return

        Actor.log.info(f'Starting crawl with {len(start_urls)} URLs.')
        Actor.log.info(f'Regex filter: {link_regex}')
        Actor.log.info(f'Limits - Max requests: {max_requests}, Max depth: {max_depth}')

        # Compile link regex
        try:
            link_pattern = re.compile(link_regex)
        except re.error as e:
            Actor.log.error(f'Invalid regular expression for linkRegex: {e}')
            return

        # Define video extensions to look for in href links
        video_extensions = ('.mp4', '.webm', '.mkv', '.m3u8', '.avi', '.mov', '.flv')

        # Initialize BeautifulSoupCrawler with input constraints
        crawler = BeautifulSoupCrawler(
            max_requests_per_crawl=max_requests,
            max_crawl_depth=max_depth,
        )

        @crawler.router.default_handler
        async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
            Actor.log.info(f'Processing {context.request.url} ...')
            
            found_videos = set()

            def resolve_url(url_str: str) -> tuple[str, str]:
                abs_url = urljoin(context.request.url, url_str)
                parsed = urlparse(abs_url)
                path = parsed.path.lower()
                return abs_url, path

            # 1. Check video tags for src
            for video in context.soup.find_all('video'):
                src = video.get('src')
                if src:
                    abs_url, _ = resolve_url(src)
                    found_videos.add(abs_url)

            # 2. Check source tags (often nested in video tags)
            for source in context.soup.find_all('source'):
                src = source.get('src')
                if src:
                    abs_url, _ = resolve_url(src)
                    found_videos.add(abs_url)

            # 3. Check a (anchor) tags ending in video extensions
            for a in context.soup.find_all('a'):
                href = a.get('href')
                if href:
                    abs_url, path = resolve_url(href)
                    if any(path.endswith(ext) for ext in video_extensions):
                        found_videos.add(abs_url)

            # If video links are found, push them to the dataset
            if found_videos:
                page_title = context.soup.title.string.strip() if context.soup.title else ""
                Actor.log.info(f'Found {len(found_videos)} video link(s) on {context.request.url}')
                await Actor.push_data({
                    "page_url": context.request.url,
                    "page_title": page_title,
                    "found_video_links": list(found_videos)
                })
            else:
                Actor.log.info(f'No video links found on {context.request.url}')

            # Enqueue follow-up links matching the regex filter and domain restriction
            await context.enqueue_links(
                include=[link_pattern],
                strategy=EnqueueStrategy.SAME_HOSTNAME
            )

        # Run the crawler
        await crawler.run(start_urls)

if __name__ == '__main__':
    asyncio.run(main())
