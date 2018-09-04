try:
    import logging, aiohttp, asyncio, bs4, discord
    from discord.ext import commands
    from urllib.parse import urlencode
except ImportError as err:
    logging.error(f"Failed to import required modules for rss.py: {err}")

class Search:
    def __init__(self, bot):
        self.bot = bot
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) Gecko/20100101 Firefox/53.0'}

    async def google_search(self, endpoint: str, header: dict):
        """Scrapes google for the top 3 results
        endpoint: Data source point.
        header: Headers to be used in ClientSession."""
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(endpoint) as resp:
                if ((resp.status) == (200)):
                    text = await resp.read()
                    soup = bs4.BeautifulSoup(text, 'html.parser')
                    results = []
                    for h3 in soup.find_all('h3', attrs={"class":"r"}):
                        for a in h3.find_all('a'):
                            if len(results) == 3:
                                return results
                            result = f"[{a.get_text()}]({a.get('href')})"
                            results.append(result)
                    await session.close()
                    return results
                else:
                    logging.error("google_search failed")
                    # Close the session if RESP is != 200. eg: Failed.
                    await session.close()
    
    @commands.command(pass_context=True)
    async def search(self, search_query):
        """Uses Google's Search Engine"""
        search_query = str(search_query.message.content).split(">search ", maxsplit=1)[1]
        if len(search_query) > 1: 
            endpoint = f"https://www.google.co.uk/search?{urlencode({'q':search_query})}&num=10&hl=en"
            results = await self.google_search(endpoint, self.header)
            embed = discord.Embed(title="Google Search Results:", colour=discord.Color.orange(),
                                description=f"Top Result: **{results[0]}**\n**More Results**\n"
                                f"{results[1]}\n{results[2]}")
            await self.bot.say(embed=embed)
        else:
            await self.bot.say(":no_entry_sign: Search function is missing search parameters")
            logging.error("Search function is missing search parameters")
    

def setup(bot):
    bot.add_cog(Search(bot))