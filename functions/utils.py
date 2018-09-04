try:
    import aiohttp, logging, bs4, json
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
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as resp:
            if ((resp.status) == (200)):
                json_resp = await resp.json()
                image_url = json_resp[key]
                await session.close()
                return image_url
            else:
                logging.error("Get image failed.")
                # Close the session if RESP is != 200. eg: Failed.
                await session.close()
 
async def file_reader(path, mode):
    """Loads json data from path specified.
    path: Path to target_file.
    mode: Mode for file to be opened in."""
    try:
        with open(path, mode) as target_file:
            data = json.load(target_file)
            target_file.close()
            return data
    except IOError:
        logging.error(f"Failed to open {path}")
        return None
