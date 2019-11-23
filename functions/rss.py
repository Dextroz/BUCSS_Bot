try:
    import feedparser, html2text, asyncio, datetime, discord, logging
    from discord.ext import commands, tasks
    from .utils import date_title, file_reader
    from config import CHANNEL_ID_NEWS
except ImportError as err:
    raise ImportError(f"Failed to import required modules for rss.py: {err}")


class Rss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_feed.start()

    async def feed_to_md(self, name: str, feed_data: dict):
        """
        Converts RSS feeds into markdown text.
        :param name: The name of the RSS feed. eg: hacker_news.
        :param feed_data: The data of the feed. eg: url and post_date from feeds.json.
        """
        # Parse RSS feed.
        d = feedparser.parse(feed_data["url"])
        # Target the first post.
        first_post = d["entries"][0]
        h = html2text.HTML2Text()
        h.ignore_images = True
        h.ignore_links = True
        summary = first_post["summary"]
        summary = h.handle(summary)
        results = []
        result = {
            "title": first_post["title"],
            "summary": summary,
            "url": first_post["link"],
            "post_date": first_post["published"],
        }
        results.append(result)
        # A list containing the dict object result.
        return results

    @tasks.loop(seconds=3600)
    async def update_feed(self):
        """
        Background task: Check RSS feeds.
        """
        feeds = await file_reader("feeds.json", "r")

        for name, feed_data in feeds.items():
            logging.debug(
                f"Checking if feed: {name} requires updating at: {datetime.datetime.now()}"
            )
            results = await self.feed_to_md(name, feed_data)
            # Checking if title is the same as date in feeds.json file.
            # If the same; do nothing.
            if (feed_data["date_title"]) == (results[0]["title"]):
                logging.debug(
                    f"Feed: {name} does not require any updates at: {datetime.datetime.now()}"
                )
                continue
            elif (feed_data["date_title"]) != (results[0]["title"]):
                logging.debug(
                    f"Feed: {name} requires updating! Running date_title for feeds.json at: {datetime.datetime.now()}"
                )
                # date_title() see utils.py
                await date_title("feeds.json", name, results[0]["title"])
                embed = discord.Embed(
                    title=results[0]["title"],
                    url=results[0]["url"],
                    description=results[0]["summary"],
                    colour=discord.Color.orange(),
                )
                embed.set_footer(text=results[0]["post_date"])
                channel = self.bot.get_channel(CHANNEL_ID_NEWS)
                await channel.send(embed=embed)

    @update_feed.before_loop
    async def before_update_feed(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def forcepost(self, ctx, feed_url: str):
        """
        Force top RSS feed post.
        :param ctx: Context provided by Discord.
        :param feed_url: The URL of the RSS feed to parse.
        """
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
            post = discord.Embed(
                title=title,
                description=summary,
                url=link,
                colour=discord.Color.orange(),
            )
            post.set_footer(text=post_date)
            await ctx.send(embed=post)
        else:
            await ctx.send(":no_entry_sign: forcepost missing feed_url parameter.")
            logging.debug("forcepost is missing feed_url parameter.")


def setup(bot):
    bot.add_cog(Rss(bot))
