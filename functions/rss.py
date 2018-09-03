try:
    import logging, json, feedparser, html2text
    from .utils import set_date
except ImportError as err:
    logging.error(f"Failed to import required modules for rss.py: {err}")


async def feed_to_md(state, name, feed_data):
    """A Function for converting rss feeds into markdown text.
    state: Either `set` or `None`: To execute set_date()
    name: Name of RSS feed object: eg: hacker_news
    feed_data: Data of the feed: URL and post_date from feeds.json"""
    # Parse rss feed.
    d = feedparser.parse(feed_data["url"])
    # Target the first post.
    first_post = d["entries"][0]
    title = first_post["title"]
    summary = first_post["summary"]
    post_date = first_post["published"]
    link = first_post["link"]
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_links = True
    summary = h.handle(summary)
    if ((state) == ("set")):
        # set_date() see utils.py
        await set_date("feeds.json", name, post_date)
    results = []
    result = {"title": title, "summary": summary,
              "url": link, "post_date": post_date}
    results.append(result)
    # A list containing the dict object result.
    return results
