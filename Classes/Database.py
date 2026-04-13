"""
SQLite-backed drop-in replacement for the Magic class.

Provides the same interface as Magic so no other code needs changing:
    db.data[edition_name]           -> EditionProxy
    db.data[edition_name].data      -> _CardDict (dict-like)
    db.data[edition_name].data[card_name] -> Card
    db.data[edition_name].code      -> set code string

Edition metadata is loaded at startup (small); card names are loaded
lazily per edition; card data is loaded lazily per card and cached.
"""
import json
import sqlite3

from .Card import Card


class _CardDict:
    """dict-like container for the cards in one edition, backed by SQLite."""

    def __init__(self, conn: sqlite3.Connection, edition_id: int):
        self._conn = conn
        self._edition_id = edition_id
        self._name_list: list | None = None   # loaded on first use
        self._cache: dict[str, Card] = {}

    # ---------------------------------------------------------------- names

    def _ensure_names(self):
        if self._name_list is None:
            cur = self._conn.execute(
                'SELECT name FROM cards WHERE edition_id = ? ORDER BY name',
                (self._edition_id,),
            )
            self._name_list = [row[0] for row in cur.fetchall()]

    def keys(self):
        self._ensure_names()
        return iter(self._name_list)

    def __iter__(self):
        return self.keys()

    def __len__(self):
        self._ensure_names()
        return len(self._name_list)

    def __contains__(self, name):
        self._ensure_names()
        return name in self._name_list

    # ---------------------------------------------------------------- cards

    def __getitem__(self, name: str) -> Card:
        if name not in self._cache:
            cur = self._conn.execute(
                'SELECT data FROM cards WHERE edition_id = ? AND name = ?',
                (self._edition_id, name),
            )
            row = cur.fetchone()
            if row is None:
                raise KeyError(name)
            self._cache[name] = Card(json.loads(row[0]))
        return self._cache[name]

    def get(self, name: str, default=None):
        try:
            return self[name]
        except KeyError:
            return default

    def items(self):
        self._ensure_names()
        for name in self._name_list:
            yield name, self[name]

    def values(self):
        self._ensure_names()
        for name in self._name_list:
            yield self[name]


class EditionProxy:
    """Wraps a SQLite editions row and exposes edition metadata as attributes."""

    def __init__(self, conn: sqlite3.Connection, edition_id: int,
                 name: str, code: str, meta_json: str):
        self.name = name
        self.code = code
        self.data = _CardDict(conn, edition_id)
        # Expose every field stored in meta as an attribute
        for k, v in json.loads(meta_json).items():
            if not hasattr(self, k):
                setattr(self, k, v)


class Database:
    """
    SQLite-backed replacement for Magic.  Identical public interface.

    Startup cost: reads ~300 KB of edition metadata (fast).
    Per-edition card names are loaded on first dropdown access.
    Per-card data is loaded on first card selection and cached.
    """

    def __init__(self, db_path: str):
        self._conn = sqlite3.connect(db_path)
        self.data: dict[str, EditionProxy] = {}

        cur = self._conn.execute(
            'SELECT id, name, code, meta FROM editions ORDER BY name'
        )
        for edition_id, name, code, meta_json in cur.fetchall():
            self.data[name] = EditionProxy(
                self._conn, edition_id, name, code or '', meta_json
            )

    def findCard(self, name: str) -> Card | None:
        cur = self._conn.execute(
            'SELECT data FROM cards WHERE name = ? LIMIT 1', (name,)
        )
        row = cur.fetchone()
        return Card(json.loads(row[0])) if row else None

    def close(self):
        self._conn.close()
