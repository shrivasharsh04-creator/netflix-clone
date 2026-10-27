"""Pull shows from the free TVMaze API and store them in our own database.

TVMaze endpoint used:
    GET https://api.tvmaze.com/shows?page=N   (250 shows per page, no API key)

Safe to re-run: shows are matched by tvmaze_id and updated in place.
"""
import re
from datetime import date

import requests
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Category, Title

TVMAZE_SHOWS_URL = "https://api.tvmaze.com/shows"
ROW_SIZE = 20

# (slug, display name) for genre rows. "Trending" and "Top Rated" are added first.
GENRE_ROWS = [
    ("action", "Action"),
    ("comedy", "Comedies"),
    ("drama", "Dramas"),
    ("science-fiction", "Sci-Fi"),
    ("crime", "Crime"),
    ("horror", "Horror"),
    ("romance", "Romance"),
    ("thriller", "Thrillers"),
]
GENRE_NAMES = {
    "action": "Action",
    "comedy": "Comedy",
    "drama": "Drama",
    "science-fiction": "Science-Fiction",
    "crime": "Crime",
    "horror": "Horror",
    "romance": "Romance",
    "thriller": "Thriller",
}

TAG_RE = re.compile(r"<[^>]+>")


def clean_html(text):
    """TVMaze summaries contain <p>, <b>, <i> tags - strip them."""
    return TAG_RE.sub("", text or "").strip()


def parse_date(value):
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


def normalise_show(show):
    """Turn one TVMaze show dict into fields for our Title model.

    Returns None if the show is missing an image or summary (it would look
    broken on the homepage).
    """
    image = show.get("image") or {}
    poster = image.get("medium") or ""
    original = image.get("original") or poster
    overview = clean_html(show.get("summary"))
    if not poster or not overview:
        return None
    return {
        "name": show.get("name", "")[:255],
        "overview": overview,
        "poster_url": poster,
        "backdrop_url": original,
        "premiered": parse_date(show.get("premiered")),
        "rating": (show.get("rating") or {}).get("average"),
        "weight": show.get("weight") or 0,
        "genres": ",".join(show.get("genres") or [])[:200],
        "official_site": show.get("officialSite") or "",
    }


def save_catalog(shows):
    """Upsert titles and rebuild category rows. Returns number of titles saved."""
    saved = []
    for show in shows:
        fields = normalise_show(show)
        if fields is None:
            continue
        title, _ = Title.objects.update_or_create(
            tvmaze_id=show["id"], defaults=fields
        )
        saved.append(title)

    def top(titles, key):
        return sorted(titles, key=key, reverse=True)[:ROW_SIZE]

    rows = [
        (
            "trending",
            "Trending Now",
            top(saved, lambda t: t.weight),
        ),
        (
            "top-rated",
            "Top Rated",
            top([t for t in saved if t.rating], lambda t: t.rating),
        ),
    ]
    for slug, display in GENRE_ROWS:
        genre = GENRE_NAMES[slug]
        matching = [t for t in saved if genre in t.genre_list and t.rating]
        rows.append((slug, display, top(matching, lambda t: t.rating)))

    for order, (slug, display, titles) in enumerate(rows):
        category, _ = Category.objects.update_or_create(
            slug=slug, defaults={"display_name": display, "order": order}
        )
        category.titles.set(titles)
    return len(saved)


class Command(BaseCommand):
    help = "Fetch shows from TVMaze and rebuild the homepage categories."

    def add_arguments(self, parser):
        parser.add_argument(
            "--pages",
            type=int,
            default=2,
            help="How many TVMaze pages to fetch (250 shows each). Default: 2",
        )

    def handle(self, *args, **options):
        shows = []
        for page in range(options["pages"]):
            self.stdout.write(f"Fetching TVMaze page {page}...")
            try:
                response = requests.get(
                    TVMAZE_SHOWS_URL, params={"page": page}, timeout=20
                )
                response.raise_for_status()
            except requests.RequestException as exc:
                raise CommandError(
                    f"Could not reach TVMaze ({exc}). Check your internet connection."
                )
            shows.extend(response.json())

        with transaction.atomic():
            count = save_catalog(shows)
        self.stdout.write(self.style.SUCCESS(f"Synced {count} titles."))
