#!/usr/bin/env python3
"""
Build a SQLite card database from an MTGJson AllSets JSON file.

Run once manually:
    python3 build_db.py

Or it is called automatically by MTGApp on first start.
Subsequent starts skip this step and query the database directly.
"""
import json
import os
import sqlite3
import sys

# Allow running from the repo root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Classes.lib import clean_unicode

DEFAULT_JSON = 'JSON Files/AllSets-x.json'
DEFAULT_DB   = 'cards.db'

_SCHEMA = """
CREATE TABLE IF NOT EXISTS editions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL UNIQUE,
    code         TEXT,
    release_date TEXT,
    meta         TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS cards (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    edition_id INTEGER NOT NULL REFERENCES editions(id),
    name       TEXT NOT NULL,
    data       TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS db_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cards_edition ON cards(edition_id);
CREATE INDEX IF NOT EXISTS idx_cards_name    ON cards(name);
"""

# Scryfall layout types that are not playable cards
_SKIP_LAYOUTS = frozenset({
    'token', 'double_faced_token', 'art_series', 'emblem',
})


def get_db_meta(db_path: str) -> dict:
    """
    Read the db_meta table from an existing database.
    Returns a plain dict (may be empty) — never raises.
    """
    if not os.path.exists(db_path):
        return {}
    try:
        conn = sqlite3.connect(db_path)
        cur  = conn.execute('SELECT key, value FROM db_meta')
        result = dict(cur.fetchall())
        conn.close()
        return result
    except Exception:
        return {}


def _scryfall_to_mtgjson(card: dict) -> dict:
    """
    Convert a Scryfall card object to the MTGJson-compatible field names
    expected by Classes.Card.
    """
    return {
        'name':        card.get('name', ''),
        'manaCost':    card.get('mana_cost', ''),
        'cmc':         card.get('cmc'),
        'colors':      card.get('colors', []),
        'type':        card.get('type_line', ''),
        'rarity':      (card.get('rarity') or '').capitalize(),
        'text':        card.get('oracle_text', ''),
        'flavor':      card.get('flavor_text', ''),
        'power':       card.get('power'),
        'toughness':   card.get('toughness'),
        'loyalty':     card.get('loyalty'),
        'artist':      card.get('artist', ''),
        'number':      card.get('collector_number', ''),
        'multiverseid': (card.get('multiverse_ids') or [None])[0],
        'layout':      card.get('layout', ''),
        'legalities':  card.get('legalities', {}),
        'printings':   card.get('set_name', ''),
    }


def build_from_scryfall(download_uri: str, db_path: str,
                        updated_at: str = '') -> None:
    """
    Download the Scryfall default_cards bulk export, group cards by set,
    and write a fresh SQLite database to db_path.

    updated_at (ISO 8601 string from the /bulk-data response) is stored in
    the db_meta table so future runs can skip the download if nothing changed.
    """
    import tempfile
    import urllib.request

    _HEADERS = {'User-Agent': 'MTGCollectionManager/3.0'}

    print('Downloading Scryfall bulk card data…')
    tmp_fd, tmp_json = tempfile.mkstemp(suffix='.json')
    try:
        os.close(tmp_fd)
        req = urllib.request.Request(download_uri, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=180) as resp:
            with open(tmp_json, 'wb') as fh:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    fh.write(chunk)

        print('Parsing card data…')
        with open(tmp_json, encoding='utf-8') as fh:
            cards = json.load(fh)
    finally:
        try:
            os.remove(tmp_json)
        except Exception:
            pass

    # Group cards by set_name, skipping non-playable layouts
    print('Grouping cards by set…')
    sets: dict[str, dict] = {}
    for card in cards:
        if card.get('layout') in _SKIP_LAYOUTS:
            continue
        set_name = card.get('set_name') or 'Unknown'
        if set_name not in sets:
            sets[set_name] = {
                'code':         card.get('set', '').lower(),
                'release_date': card.get('released_at', ''),
                'cards':        [],
            }
        sets[set_name]['cards'].append(_scryfall_to_mtgjson(card))

    print(f'Writing {len(sets)} sets to {db_path}…')
    conn = sqlite3.connect(db_path)
    conn.executescript(_SCHEMA)

    total = len(sets)
    for i, (set_name, set_data) in enumerate(sets.items(), 1):
        meta = {
            'name':        set_name,
            'code':        set_data['code'],
            'releaseDate': set_data['release_date'],
        }
        cur = conn.execute(
            'INSERT OR REPLACE INTO editions (name, code, release_date, meta) '
            'VALUES (?, ?, ?, ?)',
            (set_name, set_data['code'], set_data['release_date'],
             json.dumps(meta)),
        )
        edition_id = cur.lastrowid
        for card_data in set_data['cards']:
            conn.execute(
                'INSERT INTO cards (edition_id, name, data) VALUES (?, ?, ?)',
                (edition_id, card_data.get('name', ''), json.dumps(card_data)),
            )
        if i % 100 == 0 or i == total:
            conn.commit()
            print(f'  {i}/{total} sets…', flush=True)

    for key, value in [('last_updated', updated_at), ('source', 'scryfall')]:
        conn.execute(
            'INSERT OR REPLACE INTO db_meta (key, value) VALUES (?, ?)',
            (key, value),
        )
    conn.commit()
    conn.close()
    print(f'Database ready: {db_path}')


def build(json_path: str = DEFAULT_JSON, db_path: str = DEFAULT_DB) -> None:
    print(f'Building SQLite database from {json_path}…')

    with open(json_path, encoding='utf-8') as fh:
        raw = json.load(fh)

    # MTGJson v5 wraps everything in {"data": {...}, "meta": {...}}
    sets = raw.get('data', raw)

    conn = sqlite3.connect(db_path)
    conn.executescript(_SCHEMA)

    total = len(sets)
    for i, (_code, set_obj) in enumerate(sets.items(), 1):
        name         = clean_unicode(set_obj.get('name', _code))
        code         = set_obj.get('code', _code).lower()
        release_date = set_obj.get('releaseDate', '')
        meta         = {k: v for k, v in set_obj.items() if k != 'cards'}

        cur = conn.execute(
            'INSERT OR REPLACE INTO editions (name, code, release_date, meta) '
            'VALUES (?, ?, ?, ?)',
            (name, code, release_date, json.dumps(meta)),
        )
        edition_id = cur.lastrowid

        for card_data in set_obj.get('cards', []):
            card_name = clean_unicode(card_data.get('name', ''))
            conn.execute(
                'INSERT INTO cards (edition_id, name, data) VALUES (?, ?, ?)',
                (edition_id, card_name, json.dumps(card_data)),
            )

        if i % 50 == 0 or i == total:
            conn.commit()
            print(f'  {i}/{total} sets processed…', flush=True)

    conn.commit()
    conn.close()
    print(f'Database ready: {db_path}')


if __name__ == '__main__':
    json_arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JSON
    db_arg   = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DB
    build(json_arg, db_arg)
