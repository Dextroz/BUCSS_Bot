try:
    import asyncio, datetime, discord, logging
    from discord.ext import commands, tasks
    from config import (
        TWITTER_API_KEY,
        TWITTER_API_S,
        CHANNEL_ID_A,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_S,
    )
    from peony import PeonyClient
    from .utils import date_title, file_reader
except ImportError as err:
    raise ImportError(f"Failed to import required modules for twitter.py: {err}")


class Tweeter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = PeonyClient(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_S,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_S,
        )
        self.twitter.start()

    async def twitter_search(self, name: str):
        """
        Search twitter for a top tweet given a Twitter handle.
        :param name: The name of the Twitter handle to lookup.
        """
        resp = await self.client.api.statuses.user_timeline.get(
            count=1, screen_name=name, tweet_mode="extended"
        )
        for tweet in resp:
            results = []
            username = tweet["user"]["screen_name"]
            tweet_id = tweet["id"]
            date = tweet["created_at"]
            url = f"https://twitter.com/{username}/status/{tweet_id}"
            result = {
                "username": username,
                "text": tweet["text"],
                "url": url,
                "date": date,
            }
            results.append(result)
            return results

    @tasks.loop(seconds=3600)
    async def twitter(self):
        """
        Background task: Check Twitter.
        """
        items = await file_reader("twitter.json", "r")

        for name, data in items.items():
            logging.debug(
                f"Checking if Twitter username: {name} has posted a new tweet at: {datetime.datetime.now()}"
            )
            results = await self.twitter_search(name)
            # Checking if date_title is the same as date in twitter.json file.
            # If the same; do nothing.
            if (data["date_title"]) == (results[0]["date"]):
                logging.debug(
                    f"No new tweets for username: {name} at: {datetime.datetime.now()}"
                )
                continue
            elif (data["date_title"]) != (results[0]["date"]):
                logging.debug(
                    f"A new tweet has been for username: {name} at: {datetime.datetime.now()}"
                )
                # date_title() see utils.py
                await date_title("twitter.json", name, results[0]["date"])
                embed = discord.Embed(
                    title=results[0]["username"],
                    url=results[0]["url"],
                    description=results[0]["text"],
                    colour=discord.Color.orange(),
                )
                channel = self.bot.get_channel(CHANNEL_ID_A)
                await channel.send(embed=embed)

    @twitter.before_loop
    async def before_twitter(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Tweeter(bot))
