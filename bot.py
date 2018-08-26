try:
    import discord, logging, asyncio, feedparser, html2text, json, datetime
    from discord.ext import commands
except ImportError as err:
    print(f"Failed to import required modules: {err}")

# Setup Logging for errors.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot init.
bot = commands.Bot(command_prefix="?",
                   description="A discord bot for BUCSS", pm_help=False)


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


async def set_date(feed_name, post_date: str):
    """Set the date of latest post from rss feed"""
    try:
        with open("feeds.json", "r+") as feed_file:
            # Load json structure into memory.
            feeds = json.load(feed_file)
            for name, feed_data in feeds.items():
                if ((name) == (feed_name)):
                    # Replace value of date with post_date
                    feed_data["date"] = post_date
                    # Go to the top of feeds.json file.
                    feed_file.seek(0)
                    # Dump the new json structure to the file.
                    json.dump(feeds, feed_file, indent=2)
                    feed_file.truncate()
            feed_file.close()
    except IOError:
        logging.error("set_date(): Failed to open feeds.json.")


async def feed_to_md(name, feed_data):
    """A Function for converting rss feed into markdown text."""
    # Parse rss feed.
    d = feedparser.parse(feed_data["url"])
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
    post = f"""\n
**{title}**
*{post_date}*
\n---------------------------------------\n
{summary}
Read more at: {link}"""
    await set_date(name, post_date)
    return post


async def check_date(feed_data):
    """Function used to re-check the current date of the latest post from RSS feed."""
    d = feedparser.parse(feed_data["url"])
    # Fetch the most recent feed item.
    first_post = d["entries"][0]
    post_date = first_post["published"]
    return post_date


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
        channel = discord.Object(id="Insert channel_id here.")
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
                await bot.send_message(channel, post)
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
    post = f"""\n
**{title}**
*{post_date}*
\n---------------------------------------\n
{summary}
Read more at: {link}"""
    await bot.say(post)

# Start the background task update_feed()
bot.loop.create_task(update_feed())
bot.run("Insert Token.")
