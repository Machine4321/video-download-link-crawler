# Universal File & Video Download Link Extractor

A high-performance Apify Actor that crawls websites to discover and extract downloadable media and file links. While configured for video extensions by default (e.g. `.mp4`, `.webm`, `.m3u8`), you can customize it to extract **any file type** (e.g. `.pdf`, `.mp3`, `.zip`, `.png`, `.csv`). 

It is built using the high-performance **Crawlee for Python** library and BeautifulSoup.

## Features

- **Universal File Extraction**: Extracts file links matching any custom extensions you define from `<video src>`, `<audio src>`, `<source src>`, `<img src>`, and `<a>` tags.
- **High Performance**: Uses BeautifulSoupCrawler, which crawls pages via quick HTTP requests without running heavy headless browsers.
- **Strict RegEx Filtering**: Filters which links to enqueue and follow using custom regular expressions.
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
| `allowedExtensions` | Array | `[".mp4", ".webm", ".mkv", ".m3u8", ".avi", ".mov", ".flv"]` | Custom list of file extensions to search and extract (e.g., `[".pdf", ".mp3", ".zip"]`). |

## Output

For each page containing matching download links, the Actor outputs the results to the default dataset:

```json
{
  "page_url": "https://example.com/assets",
  "page_title": "Download Resources",
  "found_links": [
    "https://example.com/files/document.pdf",
    "https://example.com/files/audio.mp3"
  ],
  "found_video_links": [
    "https://example.com/files/document.pdf",
    "https://example.com/files/audio.mp3"
  ]
}
```
*Note: `found_video_links` is provided for backward compatibility.*

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
