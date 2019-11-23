try:
    import aiohttp, bs4, json, logging
except ImportError as err:
    raise ImportError(f"Failed to import required modules for utils.py: {err}")


async def date_title(file_name: str, object_name: str, date_title: str):
    """
    Set the date/title of latest post from a source.
    :param file_name: The name of the file to open.
    :param object_name: The name of the object to replace. Feed name of Twitter handle.
    :param date_title: The date/title to replace the existing object with.
    """
    try:
        with open(file_name, "r+") as data_file:
            # Load json structure into memory.
            feeds = json.load(data_file)
            for name, data in feeds.items():
                if (name) == (object_name):
                    # Replace value of date/title with date_title
                    data["date_title"] = date_title
                    # Go to the top of feeds.json file.
                    data_file.seek(0)
                    # Dump the new json structure to the file.
                    json.dump(feeds, data_file, indent=2)
                    data_file.truncate()
    except IOError:
        logging.debug("date_title: Failed to open requested file.")


async def get_image(endpoint: str, key: str):
    """
    Used to get images from an endpoint and return the image url.
    :param endpoint: The endpoint used to retrieve an image from.
    :param key: The key to obtain from a JSON response.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as resp:
            if (resp.status) == (200):
                json_resp = await resp.json()
                image_url = json_resp[key]
                await session.close()
                return image_url
            else:
                logging.debug("Failed to retrieve image.")
                # Close the session if RESP is != 200. eg: Failed.
                await session.close()


async def file_reader(path: str, mode: str):
    """
    Loads JSON data from the file path specified.
    :param path: The path to the target file to open.
    :param mode: The mode to open the target file in.
    """
    try:
        with open(path, mode) as target_file:
            data = json.load(target_file)
            return data
    except IOError:
        logging.debug(f"Failed to open the file: {path}")
