"""
Scryfall API integration for card data, images, and prices.

Image fetching uses a two-tier cache:
  1. In-memory dict  — fast repeat lookups within the same session.
  2. Disk cache      — persists between sessions (cache/ directory).

fetch_card_image() and all search/price functions are thread-safe.
Do NOT call ImageTk.PhotoImage() (or fetch_tk_image()) from a background thread.
"""
import hashlib
import io
import json
import os
import threading
import urllib.error
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageTk

BASE_URL   = 'https://api.scryfall.com'
CACHE_DIR  = 'cache'
_HEADERS   = {'User-Agent': 'MTGCollectionManager/3.0'}

# Cache format written to disk.  'JPEG' is smaller; 'PNG' is lossless.
CACHE_FORMAT  = 'JPEG'
CACHE_QUALITY = 90       # only used for JPEG

# In-memory image cache: (card_name, set_code, w, h, size) -> PIL Image
_mem_cache: dict = {}
_mem_lock = threading.Lock()

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


def _cache_path(card_name: str, set_code: str, w: int, h: int, size: str) -> str:
    key    = f"{card_name}|{set_code}|{w}|{h}|{size}".lower()
    digest = hashlib.md5(key.encode()).hexdigest()
    ext    = 'png' if CACHE_FORMAT == 'PNG' else 'jpg'
    return os.path.join(CACHE_DIR, f"{digest}.{ext}")


# ------------------------------------------------------------------ placeholder

def make_placeholder(width: int, height: int, text: str = 'Loading…') -> Image.Image:
    """
    Create a simple grey card-shaped placeholder image using only Pillow.
    Used while a real image is being fetched, and when no image is found.
    """
    img  = Image.new('RGB', (width, height), color=(210, 210, 210))
    draw = ImageDraw.Draw(img)
    margin = max(6, width // 16)
    draw.rounded_rectangle(
        [margin, margin, width - margin, height - margin],
        radius=max(4, width // 20),
        outline=(160, 160, 160),
        width=3,
    )
    draw.text((width // 2, height // 2), text, fill=(110, 110, 110), anchor='mm')
    return img


# ------------------------------------------------------------------ public API

def get_card(card_name: str, set_code: str = None) -> dict | None:
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


def get_card_prices(card_name: str, set_code: str = None) -> list[str]:
    """
    Return [usd, usd_foil, tix] price strings.
    Unavailable prices are 'N/A'.
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


def search_cards(query: str, page: int = 1) -> tuple[list, bool, int]:
    """
    Search Scryfall using its full query syntax.
    Returns (cards, has_more, total_cards).  cards is a list of Scryfall dicts.
    Safe to call from any thread.
    """
    params = {'q': query, 'page': page, 'order': 'name'}
    url    = f"{BASE_URL}/cards/search?{urllib.parse.urlencode(params)}"
    data   = _get_json(url)
    if data is None or data.get('object') == 'error':
        return [], False, 0
    return (
        data.get('data', []),
        data.get('has_more', False),
        data.get('total_cards', 0),
    )


def scryfall_to_card(scryfall_card: dict):
    """
    Convert a Scryfall API card dict to a local Card object suitable for
    display in ScrollFrame and the other detail panels.
    """
    from Classes.Card import Card
    data = {
        'name':        scryfall_card.get('name', ''),
        'manaCost':    scryfall_card.get('mana_cost', ''),
        'cmc':         scryfall_card.get('cmc'),
        'colors':      scryfall_card.get('colors', []),
        'type':        scryfall_card.get('type_line', ''),
        'rarity':      (scryfall_card.get('rarity') or '').capitalize(),
        'text':        scryfall_card.get('oracle_text', ''),
        'flavor':      scryfall_card.get('flavor_text', ''),
        'power':       scryfall_card.get('power'),
        'toughness':   scryfall_card.get('toughness'),
        'loyalty':     scryfall_card.get('loyalty'),
        'artist':      scryfall_card.get('artist', ''),
        'number':      scryfall_card.get('collector_number', ''),
        'multiverseid':(scryfall_card.get('multiverse_ids') or [None])[0],
        'layout':      scryfall_card.get('layout', ''),
        'legalities':  scryfall_card.get('legalities', {}),
        'printings':   scryfall_card.get('set_name', ''),
    }
    return Card({k: v for k, v in data.items() if v is not None})


# ------------------------------------------------------------------ images

def fetch_card_image(card_name: str, set_code: str, width: int, height: int,
                     scryfall_size: str = 'normal') -> Image.Image | None:
    """
    Return a PIL Image for the card using the two-tier cache.
    Lookup order: memory → disk → Scryfall network.
    Returns None on failure (caller should show a placeholder).
    Safe to call from any thread.
    """
    cache_key = (card_name, set_code or '', width, height, scryfall_size)

    with _mem_lock:
        if cache_key in _mem_cache:
            return _mem_cache[cache_key]

    disk_path = _cache_path(card_name, set_code or '', width, height, scryfall_size)
    if os.path.exists(disk_path):
        try:
            img = Image.open(disk_path).convert('RGB')
            with _mem_lock:
                _mem_cache[cache_key] = img
            return img
        except Exception:
            pass

    img = _fetch_from_scryfall(card_name, set_code, width, height, scryfall_size)
    if img is not None:
        with _mem_lock:
            _mem_cache[cache_key] = img
        try:
            save_kwargs = {'quality': CACHE_QUALITY} if CACHE_FORMAT == 'JPEG' else {}
            img.save(disk_path, CACHE_FORMAT, **save_kwargs)
        except Exception:
            pass
    return img


def _fetch_from_scryfall(card_name: str, set_code, width: int, height: int,
                          scryfall_size: str) -> Image.Image | None:
    """Download card art from Scryfall and resize it. Returns PIL Image or None."""
    card = get_card(card_name, set_code)
    if card is None:
        return None

    image_uris = card.get('image_uris')
    if not image_uris:
        faces = card.get('card_faces', [])
        if faces:
            image_uris = faces[0].get('image_uris', {})
    if not image_uris:
        return None

    image_url = image_uris.get(scryfall_size) or image_uris.get('normal')
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


def prefetch_image(card_name: str, set_code: str, width: int, height: int,
                   scryfall_size: str = 'normal') -> None:
    """
    Start a background download for a card image if it is not already cached.
    Returns immediately; the image will be in cache when needed.
    """
    cache_key = (card_name, set_code or '', width, height, scryfall_size)
    with _mem_lock:
        if cache_key in _mem_cache:
            return

    disk_path = _cache_path(card_name, set_code or '', width, height, scryfall_size)
    if os.path.exists(disk_path):
        return

    threading.Thread(
        target=fetch_card_image,
        args=(card_name, set_code, width, height, scryfall_size),
        daemon=True,
    ).start()


def fetch_tk_image(card_name: str, set_code: str, width: int, height: int) -> ImageTk.PhotoImage | None:
    """
    Fetch and convert to Tkinter PhotoImage.
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
