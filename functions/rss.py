try:
    import logging, json, feedparser, html2text, discord
except ImportError as err:
    logging.error(f"Failed to import required modules for rss.py: {err}")

async def set_date(feed_name, post_date: str):
    """Set the date of latest post from rss feed"""
    try:
        with open("feeds.json", "r+") as feed_file:
            # Load json structure into memory.
            feeds = json.load(feed_file)
            for name, feed_data in feeds.items():
                if ((name) == (feed_name)):
                    # Replace value of date with post_date
                    feed_data["date"] = post_date
                    # Go to the top of feeds.json file.
                    feed_file.seek(0)
                    # Dump the new json structure to the file.
                    json.dump(feeds, feed_file, indent=2)
                    feed_file.truncate()
            feed_file.close()
    except IOError:
        logging.error("set_date(): Failed to open feeds.json.")


async def feed_to_md(name, feed_data):
    """A Function for converting rss feed into markdown text."""
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
    # Seters for embedded post formatting.
    post = discord.Embed(title=title, description=summary, url=link, colour="FF7000")
    post.set_footer(text=post_date)
    await set_date(name, post_date)
    return post


async def check_date(feed_data):
    """Function used to re-check the current date of the latest post from RSS feed."""
    d = feedparser.parse(feed_data["url"])
    # Fetch the most recent feed item.
    first_post = d["entries"][0]
    post_date = first_post["published"]
    return post_date
