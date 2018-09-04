try:
    import logging, feedparser, html2text, asyncio, datetime, discord
    from discord.ext import commands
    from .utils import set_date, file_reader
    from config import CHANNEL_ID_NEWS
except ImportError as err:
    logging.error(f"Failed to import required modules for rss.py: {err}")

class Rss:
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel

    async def feed_to_md(self, state, name, feed_data):
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
        result = {"title": title, "summary": summary, "url": link, "post_date": post_date}
        results.append(result)
        # A list containing the dict object result.
        return results

    async def update_feed(self):
        """Background Task: Check feeds."""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            feeds = await file_reader("feeds.json", "r")

            for name, feed_data in feeds.items():
                results = await self.feed_to_md(None, name, feed_data)
                # Checking if date is the same as date in feeds.json file.
                # If the same, pass; do nothing.
                if ((feed_data["date"]) == (results[0]["post_date"])):
                    continue

                logging.info(
                    f"Running feed_to_md for {name} at {datetime.datetime.now()}")
                results = await self.feed_to_md("set", name, feed_data)
                embed = discord.Embed(title=results[0]["title"], url=results[0]["url"],
                                      description=results[0]["summary"], colour=discord.Color.orange())
                embed.set_footer(text=results[0]["post_date"])
                await self.bot.send_message(self.channel, embed=embed)

            # Sleep for 1 hour before re-checking.
            await asyncio.sleep(3600)
    
    @commands.command()
    async def forcepost(self, feed_url: str):
        """Force top feed post"""
        # Parse rss feed.
        if feed_url:
            d = feedparser.parse(feed_url)
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
            post = discord.Embed(title=title, description=summary, url=link, colour=discord.Color.orange())
            post.set_footer(text=post_date)
            await self.bot.say(embed=post)
        else:
            await self.bot.say(":no_entry_sign: forcepost missing feed_url parameter.")
            logging.error("forcepost missing feed_url parameter.")


def setup(bot):
    bot.add_cog(Rss(bot, discord.Object(id=CHANNEL_ID_NEWS)))
