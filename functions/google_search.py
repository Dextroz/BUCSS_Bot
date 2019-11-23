try:
    import aiohttp, asyncio, bs4, discord, logging
    from discord.ext import commands
    from urllib.parse import urlencode
except ImportError as err:
    raise ImportError(f"Failed to import required modules for google_search.py: {err}")


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) Gecko/20100101 Firefox/53.0"
        }

    async def google_search(self, endpoint: str, header: dict):
        """
        Scrapes Google for the top 3 search results.
        :param endpoint: Data source point.
        :param headers: Used in aiohttp ClientSession.
        """
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(endpoint) as resp:
                if (resp.status) == (200):
                    text = await resp.read()
                    soup = bs4.BeautifulSoup(text, "html.parser")
                    results = []
                    for h3 in soup.find_all("h3", attrs={"class": "r"}):
                        for a in h3.find_all("a"):
                            if len(results) == 3:
                                return results
                            result = f"[{a.get_text()}]({a.get('href')})"
                            results.append(result)
                    await session.close()
                    return results
                else:
                    logging.debug("google_search HTTP response was not 200.")
                    await session.close()

    @commands.command()
    async def search(self, ctx, *search_query: tuple):
        """
        Uses Google's search engine.
        :param ctx: Context provided by Discord.
        :param search_query: The subject to search for using Google.
        """
        search_query = " ".join(list(search_query))
        endpoint = f"https://www.google.co.uk/search?{urlencode({'q':search_query})}&num=10&hl=en"
        results = await self.google_search(endpoint, self.header)
        embed = discord.Embed(
            title="Google Search Results:",
            colour=discord.Color.orange(),
            description=f"Top Result: **{results[0]}**\n**More Results**\n"
            f"{results[1]}\n{results[2]}",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Search(bot))
