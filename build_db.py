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
CREATE INDEX IF NOT EXISTS idx_cards_edition ON cards(edition_id);
CREATE INDEX IF NOT EXISTS idx_cards_name    ON cards(name);
"""


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
