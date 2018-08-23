try:
    import discord
    import platform
    from discord.ext import commands
    import asyncio
    import feedparser
    import html2text
except ImportError:
    print("Failed to import required modules.")
description = "A discord bot to get feeds from thehackernews.com"

bot = commands.bot(command_prefix="?", description=description)


@bot.event
async def on_ready():
    print(f"""
    Logged in as {bot.user.name} ID: {bot.user.id}
    Connected to {len(bot.servers)} servers
    Connected to {bot.get_all_members()} users.
    --------
	Current Discord.py Version: {discord.__version__} | Current Python Version: {platform.python_version()}
    --------
	Use this link to invite {bot.user.name}
	https://discordapp.com/oauth2/authorize?bot_id={bot.user.id}&scope=bot&permissions=8
    """)
    # Code for showing playing status.
    return await bot.change_presence(game=discord.Game(name="Reading hackernews"))


def feed_to_md(feed: str):
    d = feedparser.parse(feed)
    # Fetch the most recent feed item.
    first_post = d["entries"][0]
    title = first_post["title"]
    summary = first_post["summary"]
    summary = html2text.html2text(summary)
    post = f"""
{title}
\n---------------------------------------\n
{summary}
"""
    return post
