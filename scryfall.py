"""
Scryfall API integration for card data, images, and prices.
Replaces the old mtgimage.com, TCGPlayer scraping, and MTGJson network code.

All functions that hit the network are safe to call from background threads,
except fetch_tk_image() which must be called from the Tkinter main thread.
"""
import io
import json
import urllib.error
import urllib.parse
import urllib.request

from PIL import Image, ImageTk

BASE_URL = 'https://api.scryfall.com'
_HEADERS = {'User-Agent': 'MTGCollectionManager/3.0'}


def _get_json(url):
    """GET a URL and return parsed JSON, or None on any error."""
    req = urllib.request.Request(url, headers=_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception:
        return None


def get_card(card_name, set_code=None):
    """
    Fetch a card from Scryfall by exact name (and optional set code).
    Returns the full Scryfall card dict, or None on failure.
    Safe to call from any thread.
    """
    params = {'exact': card_name}
    if set_code:
        params['set'] = set_code.lower()
    url = f"{BASE_URL}/cards/named?{urllib.parse.urlencode(params)}"
    return _get_json(url)


def get_card_prices(card_name, set_code=None):
    """
    Return [usd, usd_foil, tix] price strings for a card.
    Unavailable prices are represented as 'N/A'.
    Safe to call from any thread.
    """
    card = get_card(card_name, set_code)
    if card is None:
        return ['N/A', 'N/A', 'N/A']
    prices = card.get('prices', {})
    return [
        prices.get('usd') or 'N/A',
        prices.get('usd_foil') or 'N/A',
        prices.get('tix') or 'N/A',
    ]


def fetch_card_image(card_name, set_code, width, height):
    """
    Download and resize a card image from Scryfall.
    Returns a PIL Image, or None on failure.
    Safe to call from any thread — do NOT call ImageTk.PhotoImage() here.
    """
    card = get_card(card_name, set_code)
    if card is None:
        return None

    # Handle double-faced / split cards where image_uris is on each face
    image_uris = card.get('image_uris')
    if not image_uris:
        faces = card.get('card_faces', [])
        if faces:
            image_uris = faces[0].get('image_uris', {})
    if not image_uris:
        return None

    image_url = image_uris.get('normal') or image_uris.get('large')
    if not image_url:
        return None

    try:
        req = urllib.request.Request(image_url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            image_bytes = resp.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        return pil_image.resize((width, height), Image.LANCZOS)
    except Exception:
        return None


def fetch_tk_image(card_name, set_code, width, height):
    """
    Convenience wrapper that fetches and converts to a Tkinter PhotoImage.
    MUST be called from the Tkinter main thread.
    """
    pil_image = fetch_card_image(card_name, set_code, width, height)
    if pil_image is None:
        return None
    return ImageTk.PhotoImage(pil_image)


def is_internet_on():
    """Quick connectivity check against the Scryfall API."""
    try:
        req = urllib.request.Request(BASE_URL, headers=_HEADERS)
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False
