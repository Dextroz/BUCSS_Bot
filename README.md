# BUCSS_Bot
A discord bot for [BUCSS](https://www.bucss.net/) (Bournemouth University Cyber Security Society)

## Features

* Automated RSS feed reading and posting.
* Automated Twitter feed reading.
* Google search functionality
* Weather lookup functionality.
* Other useful commands: cat, dog, teams, coinflip, add and more.

## Dependancies
The bot is written in Python 3.6 so its **REQUIRED**

To install all the dependancies using pip; run the following command:
```
pip3 install -r requirements.txt
```

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

Add twitter screen name (Username) to [twitter.json](twitter.json) in the format of:
```
,
"Insert twitter screen name (username) here.": {
    "date": ""
  }
```

Configure the required variables in [config.py](config.py):
```
BOT_TOKEN = "Insert Bot Token Here."
CHANNEL_ID = "Insert Channel ID Here."
COMMAND_PREFIX = "Insert Command Prefix Here."
BOT_DESCRIPTION = "Insert Bot Description Here."
TWITTER_API_KEY = ""
TWITTER_API_S = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_TOKEN_S = ""
MAPBOX_KEY = ""
DARK_SKY_KEY = ""
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
* **A** - *Contributor* - [A](https://github.com/s5003597)

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) for details.