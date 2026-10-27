from django.db import models


class Category(models.Model):
    """One horizontal row on the homepage (e.g. Trending Now, Action)."""

    slug = models.SlugField(unique=True)
    display_name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.display_name


class Title(models.Model):
    """A TV show synced from the TVMaze API."""

    tvmaze_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)
    premiered = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    weight = models.IntegerField(default=0)  # TVMaze popularity score
    genres = models.CharField(max_length=200, blank=True)  # comma separated
    official_site = models.URLField(blank=True)
    categories = models.ManyToManyField(Category, related_name="titles", blank=True)

    def __str__(self):
        return self.name

    @property
    def genre_list(self):
        return [g for g in self.genres.split(",") if g]
