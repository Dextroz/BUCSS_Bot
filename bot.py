try:
    import discord, logging, asyncio, feedparser, html2text, json, datetime
    from discord.ext import commands
    from urllib.parse import urlencode
    from functions.rss import set_date, feed_to_md, check_date
    from functions.utils import get_image, google_search
    from config import BOT_TOKEN, CHANNEL_ID, COMMAND_PREFIX, BOT_DESCRIPTION
except ImportError as err:
    print(f"Failed to import required modules for bot.py: {err}")

# Setup Logging for errors.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
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
        channel = discord.Object(id=CHANNEL_ID)
        for name, feed_data in feeds.items():
            post_date = await check_date(feed_data)
            # Checking if date is the same as date in feeds.json file.
            # If the same, pass; do nothing.
            if ((feed_data["date"]) == (post_date)):
                pass
            # If different ie: Not equal too, run and post the feed; updating the date in feeds.json.
            elif ((feed_data["date"]) != (post_date)):
                logging.info(
                    f"Running feed_to_md for {name} at {datetime.datetime.now()}")
                post = await feed_to_md(name, feed_data)
                await bot.send_message(channel, embed=post)
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
        post = discord.Embed(title=title, description=summary, url=link, colour=discord.Color.orange())
        post.set_footer(text=post_date)
        await bot.say(embed=post)
    else:
        await bot.say("forcepost missing feed_url parameter.")

@bot.command()
async def cat():
    """Get a cool cat image"""
    endpoint = "http://aws.random.cat/meow"
    image_url = await get_image(endpoint, "file")
    embed = discord.Embed(colour=discord.Color.orange()).set_image(url=image_url)
    await bot.say(embed=embed)

@bot.command()
async def dog():
    """Get a cool dog image"""
    endpoint = "https://random.dog/woof.json"
    image_url = await get_image(endpoint, "url")
    embed = discord.Embed(colour=discord.Color.orange()).set_image(url=image_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def search(search_query):
    """Uses Google's Search Engine"""
    search_query = str(search_query.message.content).split(">search ", maxsplit=1)[1]
    if len(search_query) > 1: 
        endpoint = f"https://www.google.co.uk/search?{urlencode({'q':search_query})}&num=10&hl=en"
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) Gecko/20100101 Firefox/53.0'}
        results = await google_search(endpoint, header)
        embed = discord.Embed(title="Google Search Results:", colour=discord.Color.orange(),
                              description=f"Top Result: **{results[0]}**\n**More Results**\n"
                              f"{results[1]}\n{results[2]}")
        await bot.say(embed=embed)
    else:
        await bot.say("Search function is missing search parameters")


# Start the background task update_feed()
bot.loop.create_task(update_feed())
bot.run(BOT_TOKEN)
