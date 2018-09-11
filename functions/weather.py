try:
    import logging, aiohttp, asyncio, discord
    from discord.ext import commands
    from config import MAPBOX_KEY, DARK_SKY_KEY
except ImportError as err:
    logging.debug(f"Failed to import required modules for weather.py: {err}")


class Weather:
    def __init__(self, bot):
        self.bot = bot
        self.mapbox_key = MAPBOX_KEY
        self.darksky_key = DARK_SKY_KEY

    async def mapbox(self, location):
        """Get geocoding data from Mapbox API endpoint
        location: user specified location"""
        endpoint = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?access_token={self.mapbox_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                if ((resp.status) == (200)):
                    json_resp = await resp.json()
                    latitude = json_resp["features"][0]["center"][1]
                    longitude = json_resp["features"][0]["center"][0]
                    results = []
                    result = {"lat": latitude, "long": longitude}
                    results.append(result)
                    await session.close()
                    return results
                else:
                    logging.debug("mapbox failed.")
                    await session.close()

    async def darksky(self, results: list):
        """Get weather location from Dark Sky API endpoint.
        results: List containing dict results from mapbox"""
        exclude = "minutely,daily,hourly,alerts,flags"
        endpoint = f"https://api.darksky.net/forecast/{self.darksky_key}/{results[0]['lat']},{results[0]['long']}?exclude={exclude}&units=uk2"
        async with aiohttp.ClientSession(headers={"Accept-Encoding": "gzip"}) as session:
            async with session.get(endpoint) as resp:
                if ((resp.status) == (200)):
                    json_resp = await resp.json()
                    summary = json_resp["currently"]["summary"]
                    temperature = json_resp["currently"]["temperature"]
                    humidity = json_resp["currently"]["humidity"]
                    wind_speed = json_resp["currently"]["windSpeed"]
                    results = []
                    result = {"summary": summary, "temperature": temperature,
                              "humidity": humidity, "wind_speed": wind_speed}
                    results.append(result)
                    await session.close()
                    return results
                else:
                    logging.debug("darksky failed.")
                    await session.close()

    @commands.command(pass_context=True)
    async def weather(self, location):
        """Get weather information for a user specified location.
        location: User specified location."""
        try:
            location = location.message.content.split(">weather ", 1)[1]
            results = await self.mapbox(location)
            results = await self.darksky(results)
            embed = discord.Embed(
                title=f"Location: **__{location}__**", description=f"Current Weather - {results[0]['summary']}\nTemperature - {results[0]['temperature']}°C\nHumidity - {results[0]['humidity']}\nWind Speed - {results[0]['wind_speed']}Mph", colour=discord.Color.orange())
            embed.set_author(name="Powered By Dark Sky",
                             url="https://darksky.net/poweredby/")
            await self.bot.say(embed=embed)
        except IndexError:
            await self.bot.say(":no_entry_sign: weather function is missing location parameters")
            logging.debug("weather function is missing location parameters")


def setup(bot):
    bot.add_cog(Weather(bot))
