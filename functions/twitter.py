try:
    import logging, asyncio, datetime, discord
    from config import TWITTER_API_KEY, TWITTER_API_S, CHANNEL_ID_A
    from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_S
    from peony import PeonyClient
    from .utils import set_date, file_reader
except ImportError as err:
    logging.error(f"Failed to import required modules for rss.py: {err}")

class Tweeter:
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        self.client = PeonyClient(consumer_key=TWITTER_API_KEY,
                                  consumer_secret=TWITTER_API_S,
                                  access_token=TWITTER_ACCESS_TOKEN,
                                  access_token_secret=TWITTER_ACCESS_TOKEN_S)

    async def twitter(self):
        """Background Task: Check Twitter."""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            items = await file_reader("twitter.json", "r")

            for name, data in items.items():
                results = await self.twitter_search(None, name)
                if ((data["date"]) == (results[0]["date"])):
                    continue

                logging.info(
                        f"Running twitter_search for {name} at {datetime.datetime.now()}")
                results = await self.twitter_search("set", name)
                embed = discord.Embed(title=results[0]["username"], url=results[0]["url"],
                                    description=results[0]["text"], colour=discord.Color.orange())
                embed.set_footer(text=results[0]["date"])
                await self.bot.send_message(self.channel, embed=embed)
            # Sleep for 1 hour before re-checking.
            await asyncio.sleep(3600)
    
    async def twitter_search(self, state, name):
        """Search twitter for a top tweet
        state: Either `set` or `None`: To execute set_date()
        name: Name of the object for lookup: Twitter screen name."""
        resp = await self.client.api.statuses.user_timeline.get(count=1, 
                                                                screen_name=name,
                                                                tweet_mode="extended")
        for tweet in resp:
            results = []
            username = tweet["user"]["screen_name"]
            text = tweet["text"]
            tweet_id = tweet["id"]
            url = f"https://twitter.com/{username}/status/{tweet_id}"
            date = tweet["created_at"]
            if ((state) == ("set")):
                await set_date("twitter.json", name, date)
            result = {"username": username, "text": text, "url": url, "date": date}
            results.append(result)
            return results

def setup(bot):
    bot.add_cog(Tweeter(bot, discord.Object(id=CHANNEL_ID_A)))