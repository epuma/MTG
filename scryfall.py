"""
Scryfall API integration for card data, images, and prices.
Replaces the old mtgimage.com, TCGPlayer scraping, and MTGJson network code.

Image fetching uses a two-tier cache:
  1. In-memory dict  — fast repeat lookups within the same session.
  2. Disk cache      — persists between sessions (cache/ directory).

All functions that hit the network are safe to call from background threads,
except fetch_tk_image() which must be called from the Tkinter main thread.
"""
import hashlib
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from PIL import Image, ImageTk

BASE_URL  = 'https://api.scryfall.com'
CACHE_DIR = 'cache'
_HEADERS  = {'User-Agent': 'MTGCollectionManager/3.0'}

# In-memory image cache:  (card_name, set_code, width, height) -> PIL Image
_mem_cache: dict = {}

os.makedirs(CACHE_DIR, exist_ok=True)


# ------------------------------------------------------------------ internals

def _get_json(url: str):
    """GET a URL and return parsed JSON, or None on any error."""
    req = urllib.request.Request(url, headers=_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception:
        return None


def _cache_path(card_name: str, set_code: str, width: int, height: int) -> str:
    """Return a deterministic file path in CACHE_DIR for this image."""
    key = f"{card_name}|{set_code or ''}|{width}|{height}".lower()
    digest = hashlib.md5(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{digest}.jpg")


# ------------------------------------------------------------------ public API

def get_card(card_name: str, set_code: str = None):
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


def get_card_prices(card_name: str, set_code: str = None):
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
        prices.get('usd')      or 'N/A',
        prices.get('usd_foil') or 'N/A',
        prices.get('tix')      or 'N/A',
    ]


def fetch_card_image(card_name: str, set_code: str, width: int, height: int):
    """
    Return a PIL Image for the card, using the two-tier cache.

    Lookup order: memory → disk → Scryfall network.
    Safe to call from any thread — do NOT call ImageTk.PhotoImage() here.
    """
    cache_key = (card_name, set_code or '', width, height)

    # 1. Memory cache
    if cache_key in _mem_cache:
        return _mem_cache[cache_key]

    # 2. Disk cache
    disk_path = _cache_path(card_name, set_code or '', width, height)
    if os.path.exists(disk_path):
        try:
            img = Image.open(disk_path).convert('RGB')
            _mem_cache[cache_key] = img
            return img
        except Exception:
            pass  # Corrupt cache file — fall through to network

    # 3. Network
    img = _fetch_from_scryfall(card_name, set_code, width, height)
    if img is not None:
        _mem_cache[cache_key] = img
        try:
            img.save(disk_path, 'JPEG', quality=90)
        except Exception:
            pass  # Cache write failure is non-fatal
    return img


def _fetch_from_scryfall(card_name: str, set_code, width: int, height: int):
    """Download card art from Scryfall and resize it. Returns PIL Image or None."""
    card = get_card(card_name, set_code)
    if card is None:
        return None

    # Handle double-faced / split cards where image_uris lives on each face
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
            data = resp.read()
        img = Image.open(io.BytesIO(data)).convert('RGB')
        return img.resize((width, height), Image.LANCZOS)
    except Exception:
        return None


def fetch_tk_image(card_name: str, set_code: str, width: int, height: int):
    """
    Convenience wrapper: fetch image and convert to Tkinter PhotoImage.
    MUST be called from the Tkinter main thread.
    """
    pil_image = fetch_card_image(card_name, set_code, width, height)
    return ImageTk.PhotoImage(pil_image) if pil_image else None


def is_internet_on() -> bool:
    """Quick connectivity check against the Scryfall API."""
    try:
        req = urllib.request.Request(BASE_URL, headers=_HEADERS)
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False
