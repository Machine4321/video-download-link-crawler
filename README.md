# Video Download Link Crawler Apify Actor

This is an Apify Actor that crawls websites to discover and extract downloadable video links (e.g. `.mp4`, `.webm`, `.m3u8`, `.avi`, `.mov`, `.flv`). It is built using the high-performance **Crawlee for Python** library and BeautifulSoup.

## Features

- **High Performance**: Uses BeautifulSoupCrawler, which crawls pages via quick HTTP requests without running heavy headless browsers.
- **Strict RegEx Filtering**: Filters which links to enqueue and follow using custom regular expressions.
- **Video Extraction Logic**: Extracts video links from `<video src="...">`, `<source src="...">`, and `<a>` tags with video file extensions.
- **Hostname Scoping**: Stays within the starting website's domain to prevent wandering to third-party sites.
- **Configurable Limits**: Set max requests and max crawl depth to keep running costs low.

## Configuration

When running this Actor on the Apify platform, you can configure the following inputs:

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `startUrls` | Array | `["https://mixkit.co/free-stock-video/"]` | List of URLs to start the crawler. |
| `linkRegex` | String | `".*"` | Regex pattern to filter internal links that should be followed. |
| `maxRequests` | Integer | `50` | Maximum number of pages the crawler will request. |
| `maxDepth` | Integer | `2` | Maximum crawl depth starting from the seed URL(s). |

## Output

For each page containing video download links, the Actor outputs the results to the default dataset:

```json
{
  "page_url": "https://example.com/videos",
  "page_title": "Free Stock Videos",
  "found_video_links": [
    "https://example.com/assets/video1.mp4",
    "https://example.com/assets/video2.webm"
  ]
}
```

## Local Development

If you want to run this actor locally:

1. Install Python 3.11+.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create local storage files or configure your inputs, then run:
   ```bash
   python -m src
   ```

## Deploying to Apify Store

To deploy this Actor and start earning:

1. **Create an Actor** on your [Apify Console](https://console.apify.com/).
2. Select **Empty Python project** as the template.
3. In the web editor (Source tab), copy/paste the content of these files:
   - `src/main.py` -> `src/main.py`
   - `requirements.txt` -> `requirements.txt`
   - `.actor/INPUT_SCHEMA.json` -> `.actor/INPUT_SCHEMA.json`
4. Click **Build** to build the Docker image.
5. Once succeeded, click **Publish** to make it public.
6. Set the **Pay-Per-Event (PPE)** pricing (e.g. $1.00 per 1,000 dataset items).
