from rest_framework import serializers

from .models import Title


class TitleCardSerializer(serializers.ModelSerializer):
    """Small shape used for poster cards in rows and search results."""

    genres = serializers.ListField(source="genre_list", child=serializers.CharField())
    year = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ("id", "name", "poster_url", "rating", "genres", "year")

    def get_year(self, obj):
        return obj.premiered.year if obj.premiered else None


class TitleDetailSerializer(TitleCardSerializer):
    """Full shape used by the modal view."""

    class Meta(TitleCardSerializer.Meta):
        fields = TitleCardSerializer.Meta.fields + (
            "overview",
            "backdrop_url",
            "official_site",
        )
