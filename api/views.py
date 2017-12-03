from rest_framework.pagination import PageNumberPagination

from api.models import Name, Title
from api.serializers import TitleListSerializer, ActorTitleListSerializer
from rest_framework import generics


class TitleList(generics.ListAPIView):
    """API endpoint that allows films to be listed."""
    serializer_class = TitleListSerializer
    pagination_class = PageNumberPagination
    paginate_by = 25

    def get_queryset(self):
        """
        Lists titles of films ordered alphabetically, by filtering against a `startYear` query parameter in the URL.
        Lists also actors connected to films.
        """
        queryset = Title.objects.all()
        start_year = self.request.query_params.get('startYear', None)
        genre = self.request.query_params.get('genre', None)
        if start_year is not None:
            queryset = queryset.filter(startYear=start_year)
        if genre is not None:
            queryset = queryset.filter(genres__contains=[genre])
        return queryset.prefetch_related('name_set').order_by('primaryTitle')


class ActorTitleList(generics.ListAPIView):
    """API endpoint that allows films's of searched actor to be listed."""
    serializer_class = ActorTitleListSerializer
    pagination_class = PageNumberPagination
    paginate_by = 25

    def get_queryset(self):
        """
        Lists titles of films connected with actors, by filtering against a `name` query parameter in the URL.
        """
        queryset = Name.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(primaryName__icontains=name)
        return queryset.prefetch_related('knownForTitles').order_by('id')
