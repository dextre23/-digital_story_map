# Kitap Atlası — Book Atlas of Turkey

An interactive desktop application that maps Turkish books and their stories on a geographical map of Turkey. Browse books by province, search by title/author, read online via Open Library, and explore literary statistics.

## Features

- **Interactive Map** — Books plotted across 81 Turkish provinces with markers, clustering, and zoom
- **Search & Filter** — Find books by title, author, genre, province, or time period
- **Read Online** — Integrated Open Library reader for public-domain works
- **Statistics** — Charts by genre, publication year, author, and sentiment
- **Why Read?** — Educational articles about the value of reading
- **Multi-language** — Turkish, English, German, Spanish, French, Japanese, Russian, Chinese, Hebrew, Kyrgyz
- **Dark Theme** — Full dark-mode UI

## Requirements

- Python 3.10+
- PySide6
- requests

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Usage

1. Run `python main.py` — the app loads cached book data and shows an animated splash screen
2. Browse books on the map or use the sidebar to search/filter
3. Click a book marker to see details, description, and historical context
4. Use "Read Online" to open books via Open Library

## Project Structure

```
Kitap_Atlasi/
├── app/
│   ├── data/              # Static text content
│   ├── resources/         # QSS stylesheets
│   ├── services/          # Data, map, and API services
│   └── ui/                # All UI widgets and dialogs
├── data/                  # Cached book data (auto-generated)
├── scripts/               # Data generation tools
├── main.py                # Application entry point
└── requirements.txt       # Python dependencies
```

## Data

The book dataset contains entries mapped to Turkish provinces, including classic and modern Turkish literature with geographical, historical, and literary metadata.

## License

MIT
