try:
    import discord, logging, asyncio, feedparser, html2text, json, datetime
    from discord.ext import commands
    from functions.rss import set_date, feed_to_md, check_date
    from functions.utils import get_image
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
    post = discord.Embed(title=title, description=summary, url=link, colour="FF7000")
    post.set_footer(text=post_date)
    await bot.say(embed=post)

@bot.command()
async def cat():
    """Get a cool cat image"""
    endpoint = "http://aws.random.cat/meow"
    image_url = await get_image(endpoint, "file")
    embed = discord.Embed(colour="FF7000").set_image(url=image_url)
    await bot.say(embed=embed)

@bot.command()
async def dog():
    """Get a cool dog image"""
    endpoint = "https://random.dog/woof.json"
    image_url = await get_image(endpoint, "url")
    embed = discord.Embed(colour="FF7000").set_image(url=image_url)
    await bot.say(embed=embed)

# Start the background task update_feed()
bot.loop.create_task(update_feed())
bot.run(BOT_TOKEN)
