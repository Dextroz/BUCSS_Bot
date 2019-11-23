try:
    import discord, asyncio, logging
    from discord.ext import commands
    from random import choice
    from functions.utils import get_image

    # Import required variables from config.py
    from config import COMMAND_PREFIX, BOT_DESCRIPTION, BOT_TOKEN
except ImportError as err:
    raise ImportError(f"Failed to import required modules for bot.py: {err}")

# Bot init.
bot = commands.Bot(
    command_prefix=COMMAND_PREFIX, description=BOT_DESCRIPTION, pm_help=False
)


@bot.event
async def on_ready():
    """
    Executes on bot startup.
    """
    print(
        f"""
    Logged in as {bot.user.name} ID: {bot.user.id}
    Connected to {str(len(set(bot.get_all_members())))} users.
    --------
	Current Discord.py Version: {discord.__version__}
    --------
	Use this link to invite {bot.user.name}
    https://discordapp.com/api/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8
    """
    )
    # Code for showing playing status.
    return await bot.change_presence(activity=discord.Game("Reading RSS feeds"))


@bot.command()
async def add(ctx, left: int, right: int):
    """
    Adds two numbers together.
    :param ctx: Context provided by Discord.
    :param left: The left int to add.
    :param right: The right int to add.
    """
    await ctx.send(left + right)


@bot.command()
async def flipcoin(ctx):
    """
    Simulates flipping a coin; returning either heads or tails.
    :param ctx: Context provided by Discord.
    """
    await ctx.send(f":moneybag: {choice(['heads', 'tails'])}")


@bot.command()
async def teams(ctx, *players):
    """
    From a list of players create two teams.
    :param ctx: Context provided by Discord.
    :param players: A tuple object of players to create to teams from.
    """
    # Convert tuple to list.
    players = list(players)
    team1 = []
    team2 = []
    while len(players) > 0:
        player1 = choice(players)
        team1.append(player1)
        players.remove(player1)
        # Check if the list is empty.
        if bool(players) == False:
            continue
        player2 = choice(players)
        team2.append(player2)
        players.remove(player2)
    await ctx.send(f"**Team 1:** {team1}\n**Team 2:** {team2}")


@bot.command()
async def ping(ctx, *args):
    """
    Pongs back!
    """
    await ctx.send(":ping_pong: Pong!")


@bot.command()
async def cat(ctx):
    """
    Get a cat image.
    :param ctx: Context provided by Discord.
    """
    endpoint = "http://aws.random.cat/meow"
    image_url = await get_image(endpoint, "file")
    embed = discord.Embed(colour=discord.Color.orange()).set_image(url=image_url)
    await ctx.send(embed=embed)


@bot.command()
async def dog(ctx):
    """
    Get a dog image.
    :param ctx: Context provided by Discord.
    """
    endpoint = "https://random.dog/woof.json"
    image_url = await get_image(endpoint, "url")
    embed = discord.Embed(colour=discord.Color.orange()).set_image(url=image_url)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    # Setup logging for errors.
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)
    # Adds custom commands (COGS).
    bot.load_extension("functions.rss")
    bot.load_extension("functions.twitter")
    bot.load_extension("functions.google_search")
    bot.load_extension("functions.weather")

    # Creates RSS background task.
    rss = bot.get_cog("Rss")

    # Creates Twitter background task.
    tweeter = bot.get_cog("Tweeter")

    # Starts the bot.
    bot.run(BOT_TOKEN)
