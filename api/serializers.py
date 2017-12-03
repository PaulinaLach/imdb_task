from api.models import Name, Title
from rest_framework import serializers


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ('nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles')


class ConnectedNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ['primaryName']


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear',
                  'runtimeMinutes', 'genres')


class ConnectedTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['primaryTitle']


class TitleListSerializer(serializers.ModelSerializer):
    name_set = ConnectedNameSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear',
                  'runtimeMinutes', 'genres', 'name_set')


class ActorTitleListSerializer(serializers.ModelSerializer):
    knownForTitles = ConnectedTitleSerializer(read_only=True, many=True)

    class Meta:
        model = Name
        fields = ('nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles')



