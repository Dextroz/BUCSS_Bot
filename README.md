# BUCSS_Bot
A discord bot for [BUCSS](https://www.bucss.net/) (Bournemouth University Cyber Security Society)

## Features

* Automated RSS feed reading and posting.
* Automated Twitter feed reading.
* Google search functionality
* Weather lookup functionality.
* Other useful commands: cat, dog, teams, coinflip, add and more.

## Dependencies
The bot is written in Python 3.7.5 so its **REQUIRED**

To install all the dependencies using pip; run the following command:
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
    "date_title": ""
  }
```

Add twitter screen name (Username) to [twitter.json](twitter.json) in the format of:
```
,
"Insert twitter screen name (username) here.": {
    "date_title": ""
  }
```

Configure the required variables in [config.py](config.py):
```
BOT_TOKEN = "Insert Bot Token Here."
CHANNEL_ID_A = 
CHANNEL_ID_NEWS = 
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

1. Head to [discord application](https://discordapp.com/developers/applications/) and click **New Application**.
2. Provide a *Name* for the application and click **Create**.
3. On the left panel, select *Bot*.
4. Click **Add Bot**.
5. Click **Yes, do it!**.
6. Once created, copy the bots token and place it in [config.py](config.py).
7.Execute the [bot.py](bot.py) and go to the link provided in the console:
    Should look something like: `https://discordapp.com/api/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8`
8. Select the server for the bot to be added to.
9. Congratulations, you have now added the bot to your server!

### Container

* Complete all the prerequisites before running these commands.

1. `sudo podman build -t bucss_bot .`

2. `sudo podman run --rm -t bucss_bot`

## Authors -- Contributors

* **dbrennand** - *Author* - [dbrennand](https://github.com/dbrennand)
* **A** - *Contributor* - [A](https://github.com/s5003597)

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) for details.