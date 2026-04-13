# MTG Collection Manager

A desktop application for tracking your Magic: The Gathering card collection.
Browse cards by set, view artwork and card details, track quantities and notes,
and monitor market prices — all powered by the free [Scryfall API](https://scryfall.com/docs/api).

---

## Requirements

- **Python 3.8+**
- **Pillow** (image processing) — the only third-party dependency

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/epuma/MTG.git
cd MTG
```

### 2. (Recommended) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the app

```bash
python3 MTGApp.py
```

**First run only:** the app will build a local SQLite database (`cards.db`)
from the included `JSON Files/AllSets-x.json`. This takes about 30–60 seconds
and only happens once. Subsequent starts are fast.

---

## Features

| Feature | Description |
|---|---|
| **Browse by set** | Select any MTG edition and card from the dropdowns |
| **Card filter** | Type in the Filter box to narrow the card dropdown in real time |
| **Card details** | Scrollable panel showing all card attributes |
| **Card artwork** | Downloaded from Scryfall and cached locally in `cache/` |
| **Live prices** | Market, Foil, and MTGO prices fetched from Scryfall |
| **Price history** | Last 10 price snapshots stored per owned card |
| **Collections** | Open/save `.json` collection files to track quantities and notes |
| **Stats bar** | Total cards owned, unique cards, and estimated market value |
| **Scryfall search** | Full Scryfall query syntax via **View → Search Scryfall…** |
| **Collection grid** | Visual thumbnail overview via **View → Collection Overview…** |
| **CSV export** | Export owned cards via **File → Export as CSV…** |

---

## Keyboard shortcuts

| Keys | Action |
|---|---|
| `Enter` | Load the selected card |
| `Alt + ←` / `Alt + →` | Previous / next card |
| `Alt + ↑` / `Alt + ↓` | Previous / next edition |
| `Ctrl + N` | New collection |
| `Ctrl + O` | Open collection |
| `Ctrl + S` | Save collection |
| `Ctrl + E` | Export as CSV |

A full reference is also available under **Help → Keyboard Shortcuts**.

---

## Collection files

Collections are plain `.json` files you create via **File → New**.
The included `eric_collection.json` is a sample you can open to explore
the interface without setting up your own collection first.

---

## Updating the card database

The included `JSON Files/AllSets-x.json` is a snapshot of the MTGJson
database. To update it:

1. Download the latest `AllSets.json` from [mtgjson.com](https://mtgjson.com)
   and replace `JSON Files/AllSets-x.json`.
2. In the app, go to **Help → Rebuild Database…** to regenerate `cards.db`.
3. Restart the app.

---

## Image cache

Card artwork is downloaded from Scryfall on first view and stored in `cache/`
as JPEG files. The cache persists between sessions. To clear it, delete the
`cache/` folder — images will be re-downloaded as needed.

Cache format and quality can be tuned at the top of `scryfall.py`:

```python
CACHE_FORMAT  = 'JPEG'   # or 'PNG' for lossless
CACHE_QUALITY = 90       # JPEG quality (1–95)
```
