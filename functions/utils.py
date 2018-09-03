try:
    import aiohttp, logging, bs4, json
    from peony import PeonyClient
except ImportError as err:
    logging.error(f"Failed to import required modules for utils.py: {err}")


async def set_date(file_name, object_name, post_date: str):
    """Set the date of latest post from a source.
    file_name: File name to open.
    Object_name: Name of the object: rss: hacker_news or twitter screen name.
    post_date: Date of the object being posted."""
    try:
        with open(file_name, "r+") as data_file:
            # Load json structure into memory.
            items = json.load(data_file)
            for name, data in items.items():
                if ((name) == (object_name)):
                    # Replace value of date with post_date
                    data["date"] = post_date
                    # Go to the top of feeds.json file.
                    data_file.seek(0)
                    # Dump the new json structure to the file.
                    json.dump(items, data_file, indent=2)
                    data_file.truncate()
            data_file.close()
    except IOError:
        logging.error("set_date(): Failed to open requested file.")


async def get_image(endpoint: str, key: str):
    """Used to get images from an endpoint and return the image url.
    key: Key to obtained from json_resp (json object).
    endpoint: Data source point."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as resp:
                if ((resp.status) == (200)):
                    json_resp = await resp.json()
                    image_url = json_resp[key]
                    return image_url
                else:
                    logging.error("Get image failed.")
    finally:
        await session.close()


async def google_search(endpoint: str, header: dict):
    """Scrapes google for the top 3 results
    endpoint: Data source point.
    header: Headers to be used in ClientSession."""
    try:
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(endpoint) as resp:
                if ((resp.status) == (200)):
                    text = await resp.read()
                    soup = bs4.BeautifulSoup(text, 'html.parser')
                    results = []
                    for h3 in soup.find_all('h3', attrs={"class": "r"}):
                        for a in h3.find_all('a'):
                            if len(results) == 3:
                                return results
                            result = f"[{a.get_text()}]({a.get('href')})"
                            results.append(result)
                    return results
                else:
                    logging.error("google_search failed")
    finally:
        await session.close()


async def twitter_search(state, name, twitter_keys: dict):
    """Search twitter for a top tweet
    state: Either `set` or `None`: To execute set_date()
    name: Name of the object for lookup: Twitter screen name.
    twitter_keys: dict object of twitter keys. Passed into PeonyClient."""
    try:
        async with aiohttp.ClientSession() as session:
            client = PeonyClient(consumer_key=twitter_keys["keys"][0],
                                 consumer_secret=twitter_keys["keys"][1],
                                 access_token=twitter_keys["keys"][2],
                                 access_token_secret=twitter_keys["keys"][3], session=session)
            resp = await client.api.statuses.user_timeline.get(count=1, screen_name=name, tweet_mode="extended")
        for tweet in resp:
            results = []
            username = tweet["user"]["screen_name"]
            text = tweet["text"]
            tweet_id = tweet["id"]
            url = f"https://twitter.com/{username}/status/{tweet_id}"
            date = tweet["created_at"]
            if ((state) == ("set")):
                await set_date("twitter.json", name, date)
            result = {"username": username,
                      "text": text, "url": url, "date": date}
            results.append(result)
            return results
    finally:
        await session.close()
