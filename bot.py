try:
    import discord, logging, asyncio
    from discord.ext import commands
    from functions.utils import get_image
    # Import all vars from config.py
    from config import COMMAND_PREFIX, BOT_DESCRIPTION, BOT_TOKEN
except ImportError as err:
    print(f"Failed to import required modules for bot.py: {err}")

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

@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together"""
    await bot.say(left + right)


@bot.command()
async def ping(*args):
    """Pongs back!"""
    await bot.say(":ping_pong: Pong!")


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

    
if __name__ == "__main__":
    # Setup Logging for errors.
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    # Adds Custom Commands (COGS)
    bot.load_extension('functions.rss')
    bot.load_extension('functions.twitter')
    bot.load_extension('functions.google_search')

    # Creates RSS Background Task
    rss = bot.get_cog('Rss')
    bot.loop.create_task(rss.update_feed())

    # Creates Twitter Background Task
    tweeter = bot.get_cog('Tweeter')
    bot.loop.create_task(tweeter.twitter())

    # Starts the bot
    bot.run(BOT_TOKEN)
