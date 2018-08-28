try:
    import aiohttp, logging
except ImportError as err:
    logging.error(f"Failed to import required modules for utils.py: {err}")

async def get_image(endpoint: str, key: str):
    """Used to get images from an endpoint and return the image url."""
    async with aiohttp.get(endpoint) as resp:
        if ((resp.status) == (200)):
            json_resp = await resp.json()
            image_url = json_resp[key]
            return image_url
        else:
            logging.error("Get image failed.")
