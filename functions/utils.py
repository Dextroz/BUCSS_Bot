try:
    import aiohttp, logging, bs4
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

async def google_search(endpoint: str, header: dict):
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(endpoint) as resp:
            if ((resp.status) == (200)):
                text = await resp.read()
                soup = bs4.BeautifulSoup(text, 'html.parser')
                results = []
                for h3 in soup.find_all('h3', attrs={"class":"r"}):
                    for a in h3.find_all('a'):
                        if len(results) == 3:
                            return results
                        result = f"[{a.get_text()}]({a.get('href')})"
                        results.append(result)
                return results
            else:
                logging.error("google_search failed")