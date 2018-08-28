# BUCSS_Bot
A discord bot for [BUCSS](https://www.bucss.net/) (Bournemouth University Cyber Security Society)

## Dependancies
The bot is written in Python 3.6 so its **REQUIRED**

It requires the following packages:

1. discord.py
2. asyncio
3. feedparser
4. html2text
5. aiohttp

## Contributing!
**All pull requests are welcome!**

## Prerequisites

Add rss feeds to [feeds.json](feeds.json) in the format of:
```
,
"Insert a title here": {
    "url": "Insert RSS feed url here.",
    "date": ""
  }
```

Configure the required variables in [config.py](config.py):
```
BOT_TOKEN = "Insert Bot Token Here."
CHANNEL_ID = "Insert Channel ID Here."
COMMAND_PREFIX = "Insert Command Prefix Here."
BOT_DESCRIPTION = "Insert Bot Description Here."
```

To use the bot do the following:

1. Head to [discord application](https://discordapp.com/developers/applications/) and select an **create an application**.
2. Under settings select bot; See image below:

![bot.png](bot.png)

4. Execute the [bot.py](bot.py) and go to the link provided in the console:
    Should look something like: `https://discordapp.com/api/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8`
5. Select the server for the bot to be added to.

## Authors -- Contributors

* **Daniel Brennand** - *Author* - [Dextroz](https://github.com/Dextroz)

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) for details.