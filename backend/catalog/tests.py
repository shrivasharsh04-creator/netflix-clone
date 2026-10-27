from django.test import TestCase

from .management.commands.sync_catalog import clean_html, save_catalog
from .models import Title


def fake_show(i, genres, rating=7.0, image=True, summary="<p>A <b>great</b> show.</p>"):
    return {
        "id": i,
        "name": f"Show {i}",
        "genres": genres,
        "premiered": "2020-01-01",
        "rating": {"average": rating},
        "weight": 100 - i,
        "image": {"medium": f"https://x/m{i}.jpg", "original": f"https://x/o{i}.jpg"} if image else None,
        "summary": summary,
        "officialSite": "",
    }


class CatalogTests(TestCase):
    def setUp(self):
        shows = [fake_show(i, ["Action", "Drama"], rating=5 + i / 10) for i in range(1, 6)]
        shows.append(fake_show(50, ["Comedy"], image=False))  # skipped: no image
        shows.append(fake_show(51, ["Comedy"], summary=None))  # skipped: no summary
        save_catalog(shows)

    def test_clean_html(self):
        self.assertEqual(clean_html("<p>A <b>great</b> show.</p>"), "A great show.")

    def test_skips_incomplete_shows(self):
        self.assertEqual(Title.objects.count(), 5)

    def test_sync_is_rerunnable(self):
        save_catalog([fake_show(1, ["Action"])])
        self.assertEqual(Title.objects.count(), 5)

    def test_homepage(self):
        data = self.client.get("/api/homepage/").json()
        self.assertIsNotNone(data["hero"])
        slugs = [r["slug"] for r in data["rows"]]
        self.assertEqual(slugs[:2], ["trending", "top-rated"])
        self.assertTrue(data["rows"][0]["titles"])

    def test_detail(self):
        pk = Title.objects.first().pk
        self.assertEqual(self.client.get(f"/api/titles/{pk}/").status_code, 200)
        self.assertEqual(self.client.get("/api/titles/99999/").status_code, 404)

    def test_search(self):
        self.assertEqual(len(self.client.get("/api/search/?q=show 3").json()), 1)
        self.assertEqual(self.client.get("/api/search/?q=").status_code, 400)
        self.assertEqual(self.client.get("/api/search/").status_code, 400)
