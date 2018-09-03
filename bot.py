try:
    import discord, logging, asyncio, feedparser, html2text, json, datetime
    from discord.ext import commands
    from urllib.parse import urlencode
    from functions.rss import feed_to_md
    from functions.utils import get_image, google_search, twitter_search
    # Import all vars from config.py
    from config import *
except ImportError as err:
    print(f"Failed to import required modules for bot.py: {err}")

# Setup Logging for errors.
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot init.
bot = commands.Bot(command_prefix=COMMAND_PREFIX,
                   description=BOT_DESCRIPTION, pm_help=False)


@bot.event
async def on_ready():
    """Executes when bot is starting up"""
    print(f"""
    Logged in as {bot.user.name} ID: {bot.user.id}
    Connected to {str(len(bot.servers))} servers
    Connected to {str(len(set(bot.get_all_members())))} users.
    --------
	Current Discord.py Version: {discord.__version__}
    --------
	Use this link to invite {bot.user.name}
    https://discordapp.com/api/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8
    """)
    # Code for showing playing status.
    return await bot.change_presence(game=discord.Game(name="Reading Hacking News."))


async def update_feed():
    """Background Task: Check feeds."""
    await bot.wait_until_ready()
    while not bot.is_closed:
        try:
            with open("feeds.json", "r") as feed_file:
                feeds = json.load(feed_file)
                feed_file.close()
        except IOError:
            logging.error("Failed to open feeds.json")
        channel = discord.Object(id=CHANNEL_ID_NEWS)
        for name, feed_data in feeds.items():
            results = await feed_to_md(None, name, feed_data)
            # Checking if date is the same as date in feeds.json file.
            # If the same, pass; do nothing.
            if ((feed_data["date"]) == (results[0]["post_date"])):
                pass
            # If different ie: Not equal too, run and post the feed; updating the date in feeds.json.
            elif ((feed_data["date"]) != (results[0]["post_date"])):
                logging.info(
                    f"Running feed_to_md for {name} at {datetime.datetime.now()}")
                results = await feed_to_md("set", name, feed_data)
                embed = discord.Embed(title=results[0]["title"], url=results[0]["url"],
                                      description=results[0]["summary"], colour=discord.Color.orange())
                embed.set_footer(text=results[0]["post_date"])
                await bot.send_message(channel, embed=embed)
        # Sleep for 1 hour before re-checking.
        await asyncio.sleep(3600)


async def twitter():
    """Background Task: Check Twitter."""
    await bot.wait_until_ready()
    while not bot.is_closed:
        try:
            with open("twitter.json", "r") as twitter_file:
                items = json.load(twitter_file)
                twitter_file.close()
        except IOError:
            logging.error("Failed to open twitter.json")
        channel = discord.Object(id=CHANNEL_ID_A)
        twitter_keys = {"keys": [TWITTER_API_KEY, TWITTER_API_S,
                                 TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_S]}
        for name, data in items.items():
            results = await twitter_search(None, name, twitter_keys)
            if ((data["date"]) == (results[0]["date"])):
                pass
            elif ((data["date"]) != (results[0]["date"])):
                logging.info(
                    f"Running twitter_search for {name} at {datetime.datetime.now()}")
                results = await twitter_search("set", name, twitter_keys)
                embed = discord.Embed(title=results[0]["username"], url=results[0]["url"],
                                      description=results[0]["text"], colour=discord.Color.orange())
                embed.set_footer(text=results[0]["date"])
                await bot.send_message(channel, embed=embed)
            # Sleep for 1 hour before re-checking.
            await asyncio.sleep(3600)

# Other bot commands below.


@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together"""
    await bot.say(left + right)


@bot.command()
async def ping(*args):
    """Pongs back!"""
    await bot.say(":ping_pong: Pong!")


@bot.command()
async def forcepost(feed_url: str):
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
        post = discord.Embed(title=title, description=summary,
                             url=link, colour=discord.Color.orange())
        post.set_footer(text=post_date)
        await bot.say(embed=post)
    else:
        await bot.say(":no_entry_sign: forcepost missing feed_url parameter.")
        logging.error("forcepost missing feed_url parameter.")


@bot.command()
async def cat():
    """Get a cool cat image"""
    endpoint = "http://aws.random.cat/meow"
    image_url = await get_image(endpoint, "file")
    embed = discord.Embed(colour=discord.Color.orange()
                          ).set_image(url=image_url)
    await bot.say(embed=embed)


@bot.command()
async def dog():
    """Get a cool dog image"""
    endpoint = "https://random.dog/woof.json"
    image_url = await get_image(endpoint, "url")
    embed = discord.Embed(colour=discord.Color.orange()
                          ).set_image(url=image_url)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def search(search_query):
    """Uses Google's Search Engine"""
    search_query = str(search_query.message.content).split(
        ">search ", maxsplit=1)[1]
    if len(search_query) > 1:
        endpoint = f"https://www.google.co.uk/search?{urlencode({'q':search_query})}&num=10&hl=en"
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) Gecko/20100101 Firefox/53.0'}
        results = await google_search(endpoint, header)
        embed = discord.Embed(title="Google Search Results:", colour=discord.Color.orange(),
                              description=f"Top Result: **{results[0]}**\n**More Results**\n"
                              f"{results[1]}\n{results[2]}")
        await bot.say(embed=embed)
    else:
        await bot.say(":no_entry_sign: Search function is missing search parameters")
        logging.error("Search function is missing search parameters")


# Start the background task update_feed()
bot.loop.create_task(update_feed())
bot.loop.create_task(twitter())
bot.run(BOT_TOKEN)
