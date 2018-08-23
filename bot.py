try:
    import discord
    import logging
    import platform
    from discord.ext import commands
    import asyncio
    import feedparser
    import html2text
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
                   description="A discord bot to get feeds from thehackernews.com")


@bot.event
async def on_ready():
    print(f"""
    Logged in as {bot.user.name} ID: {bot.user.id}
    Connected to {len(bot.servers)} servers
    Connected to {len(bot.get_all_members())} users.
    --------
	Current Discord.py Version: {discord.__version__} | Current Python Version: {platform.python_version()}
    --------
	Use this link to invite {bot.user.name}
	https://discordapp.com/oauth2/authorize?bot_id={bot.user.id}&scope=bot&permissions=8
    """)
    # Code for showing playing status.
    return await bot.change_presence(game=discord.Game(name="Reading thehackernews.com"))


def set_date(post_date: str):
    try:
        with open("./date.txt", "w+") as date_file:
            date_file.write(post_date)
            date_file.close()
    except IOError:
        logging.error("Failed to open/set post date.")


def feed_to_md(feed_url: str):
    d = feedparser.parse(feed_url)
    # Fetch the most recent feed item.
    first_post = d["entries"][0]
    title = first_post["title"]
    summary = first_post["summary"]
    post_date = first_post["published"]
    summary = html2text.html2text(summary)
    post = f"""
{title}
{post_date}
\n---------------------------------------\n
{summary}
"""
    set_date(post_date)
    return post

"""
Used to re-check the current date of the latest post from RSS feed.
"""
def check_date(feed_url: str):
    d = feedparser.parse(feed_url)
    # Fetch the most recent feed item.
    first_post = d["entries"][0]
    post_date = first_post["published"]
    return post_date


async def background_task():
    await bot.wait_until_ready()
    channel = discord.Object(id='Insert channel_id here.')
    # Send init message.
    await bot.send_message(channel, feed_to_md("https://thehackernews.com/feeds/posts/default"))
    while not bot.is_closed:
        # Check the top post's date from RSS feed.
        post_date = await check_date("https://thehackernews.com/feeds/posts/default")
        try:
            with open("./date.txt", "r") as date_file:
                # The date of first post, stored in date.txt
                data = date_file.read()
                if ((data) == (post_date)):
                    # If date is still the same, do nothing ie: pass.
                    pass
                elif ((data) != (post_date)):
                    # if dates are different 
                    await bot.send_message(channel, feed_to_md("https://thehackernews.com/feeds/posts/default"))
                date_file.close()
        except IOError:
            logging.error("Failed to open/read data.txt")
        # Sleep for 1 hour before re-checking.
        await asyncio.sleep(3600)


bot.loop.create_task(background_task())
bot.run("Insert You're Token Here.")
