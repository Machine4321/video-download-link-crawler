import asyncio
import re
from urllib.parse import urljoin, urlparse

from apify import Actor
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
        allowed_extensions = actor_input.get('allowedExtensions', ['.mp4', '.webm', '.mkv', '.m3u8', '.avi', '.mov', '.flv'])

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

        # Normalize allowed extensions to lowercase and ensure they start with a dot
        normalized_extensions = []
        for ext in allowed_extensions:
            ext_str = str(ext).strip().lower()
            if ext_str:
                if not ext_str.startswith('.'):
                    ext_str = '.' + ext_str
                normalized_extensions.append(ext_str)

        if not normalized_extensions:
            normalized_extensions = ['.mp4', '.webm', '.mkv', '.m3u8', '.avi', '.mov', '.flv']

        Actor.log.info(f'Starting crawl with {len(start_urls)} URLs.')
        Actor.log.info(f'Regex filter: {link_regex}')
        Actor.log.info(f'Target file extensions: {normalized_extensions}')
        Actor.log.info(f'Limits - Max requests: {max_requests}, Max depth: {max_depth}')

        # Compile link regex
        try:
            link_pattern = re.compile(link_regex)
        except re.error as e:
            Actor.log.error(f'Invalid regular expression for linkRegex: {e}')
            return

        # Initialize BeautifulSoupCrawler with input constraints
        crawler = BeautifulSoupCrawler(
            max_requests_per_crawl=max_requests,
            max_crawl_depth=max_depth,
        )

        @crawler.router.default_handler
        async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
            Actor.log.info(f'Processing {context.request.url} ...')
            
            found_links = set()

            def resolve_url(url_str: str) -> tuple[str, str]:
                abs_url = urljoin(context.request.url, url_str)
                parsed = urlparse(abs_url)
                path = parsed.path.lower()
                return abs_url, path

            # Extract URLs from video, audio, source, img and anchor tags matching extensions
            tags_to_check = {
                'video': 'src',
                'audio': 'src',
                'source': 'src',
                'img': 'src',
                'a': 'href'
            }

            for tag_name, attr_name in tags_to_check.items():
                for element in context.soup.find_all(tag_name):
                    val = element.get(attr_name)
                    if val:
                        abs_url, path = resolve_url(val)
                        if any(path.endswith(ext) for ext in normalized_extensions):
                            found_links.add(abs_url)

            # If links are found, push them to the dataset
            if found_links:
                page_title = context.soup.title.string.strip() if context.soup.title else ""
                Actor.log.info(f'Found {len(found_links)} matching link(s) on {context.request.url}')
                await Actor.push_data({
                    "page_url": context.request.url,
                    "page_title": page_title,
                    "found_links": list(found_links),
                    "found_video_links": list(found_links)  # Backward compatibility
                })
            else:
                Actor.log.info(f'No matching links found on {context.request.url}')

            # Enqueue follow-up links matching the regex filter and domain restriction
            await context.enqueue_links(
                include=[link_pattern],
                strategy='same-hostname'
            )

        # Run the crawler
        await crawler.run(start_urls)

if __name__ == '__main__':
    asyncio.run(main())
