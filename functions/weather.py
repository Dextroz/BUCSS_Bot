try:
    import aiohttp, asyncio, discord, logging
    from discord.ext import commands
    from config import MAPBOX_KEY, DARK_SKY_KEY
except ImportError as err:
    raise ImportError(f"Failed to import required modules for weather.py: {err}")


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mapbox_key = MAPBOX_KEY
        self.darksky_key = DARK_SKY_KEY

    async def mapbox(self, location: str):
        """
        Get geocoding data from the Mapbox API endpoint.
        :param location: The user specified location.
        """
        endpoint = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={self.mapbox_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                if (resp.status) == (200):
                    json_resp = await resp.json()
                    results = []
                    result = {
                        "lat": json_resp["features"][0]["center"][1],
                        "long": json_resp["features"][0]["center"][0],
                    }
                    results.append(result)
                    await session.close()
                    return results
                else:
                    logging.debug("Mapbox failed to retrieve location data.")
                    await session.close()

    async def darksky(self, results: list):
        """
        Get weather location from the Dark Sky API.
        :param results: A List containing dict results from Mapbox API.
        """
        exclude = "minutely,daily,hourly,alerts,flags"
        endpoint = f"https://api.darksky.net/forecast/{self.darksky_key}/{results[0]['lat']},{results[0]['long']}?exclude={exclude}&units=uk2"
        async with aiohttp.ClientSession(
            headers={"Accept-Encoding": "gzip"}
        ) as session:
            async with session.get(endpoint) as resp:
                if (resp.status) == (200):
                    json_resp = await resp.json()
                    results = []
                    result = {
                        "summary": json_resp["currently"]["summary"],
                        "temperature": json_resp["currently"]["temperature"],
                        "humidity": json_resp["currently"]["humidity"],
                        "wind_speed": json_resp["currently"]["windSpeed"],
                    }
                    results.append(result)
                    await session.close()
                    return results
                else:
                    logging.debug("Dark Sky failed to retrieve location data.")
                    await session.close()

    @commands.command()
    async def weather(self, ctx, location: str):
        """
        Get weather information for a user specified location.
        :param ctx: Context provided by Discord.
        :param location: A user specified location to retrieve weather data for.
        """
        try:
            results = await self.mapbox(location)
            results = await self.darksky(results)
            embed = discord.Embed(
                title=f"Location: **__{location}__**",
                description=f"Current Weather - {results[0]['summary']}\nTemperature - {results[0]['temperature']}°C\nHumidity - {results[0]['humidity']}\nWind Speed - {results[0]['wind_speed']}Mph",
                colour=discord.Color.orange(),
            )
            embed.set_author(
                name="Powered By Dark Sky", url="https://darksky.net/poweredby/"
            )
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(
                ":no_entry_sign: weather function is missing location parameters"
            )
            logging.debug("weather function is missing location parameters")


def setup(bot):
    bot.add_cog(Weather(bot))
