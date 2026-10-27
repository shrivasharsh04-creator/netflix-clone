from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Title
from .serializers import TitleCardSerializer, TitleDetailSerializer

ROW_SIZE = 20


def _ordered_titles(category):
    # "Trending" follows TVMaze popularity; every other row follows rating.
    order = "-weight" if category.slug == "trending" else "-rating"
    return category.titles.order_by(order, "name")[:ROW_SIZE]


@api_view(["GET"])
def homepage(request):
    categories = Category.objects.all()
    rows = []
    for category in categories:
        titles = _ordered_titles(category)
        rows.append(
            {
                "slug": category.slug,
                "display_name": category.display_name,
                "titles": TitleCardSerializer(titles, many=True).data,
            }
        )

    hero = None
    # Hero = most popular title that has a summary and an image.
    hero_title = (
        Title.objects.exclude(overview="")
        .exclude(backdrop_url="")
        .order_by("-weight", "-rating")
        .first()
    )
    if hero_title:
        hero = TitleDetailSerializer(hero_title).data

    return Response({"hero": hero, "rows": rows})


@api_view(["GET"])
def title_detail(request, pk):
    title = get_object_or_404(Title, pk=pk)
    return Response(TitleDetailSerializer(title).data)


@api_view(["GET"])
def search(request):
    query = request.query_params.get("q", "").strip()
    if not query:
        return Response({"detail": "Query parameter 'q' is required."}, status=400)
    results = Title.objects.filter(
        Q(name__icontains=query) | Q(genres__icontains=query)
    ).order_by("-rating")[:30]
    return Response(TitleCardSerializer(results, many=True).data)
