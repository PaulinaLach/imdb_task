import json

from api.models import Name, Title, KnownFor
from api.views import TitleList, ActorTitleList
from django.test import Client, RequestFactory, TestCase


class BasicTest(TestCase):
    """Basic test cases."""
    def setUp(self):
        self.factory = RequestFactory()
        self.film1 = Title.objects.create(
            tconst="tt1601394",
            titleType="tvEpisode",
            primaryTitle="ZZZ",
            originalTitle="1969 Oscar Awards",
            isAdult=False,
            startYear=1969,
            endYear=None,
            runtimeMinutes=None,
            genres=["Biography", "Documentary", "Music"]
        )
        self.film2 = Title.objects.create(
            tconst="tt4024486",
            titleType="tvEpisode",
            primaryTitle="AAA",
            originalTitle="A Couple of Brians-Two Poets",
            isAdult=False,
            startYear=1969,
            endYear=None,
            runtimeMinutes=None,
            genres=["Biography", "Documentary", "Music"]
        )
        self.name1 = Name.objects.create(
            nconst="nm0000001",
            primaryName="Fred Astaire",
            birthYear=1899,
            deathYear=1987
        )
        self.name2 = Name.objects.create(
            nconst="nm0000001",
            primaryName="Lauren Bacall",
            birthYear=1924,
            deathYear=2014
        )
        KnownFor.objects.create(name=self.name1, title=self.film1)

    def test_response(self):
        """Tests if response code matches."""
        request = self.factory.get('/titles?startYear=1969')

        response = TitleList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_alphabetical_order(self):
        """Tests if the result is in the alphabetical order."""
        request = self.factory.get('/titles?startYear=1969')
        response = TitleList.as_view()(request)

        response.render()
        rendered_json = json.loads(response.content)
        self.assertEqual(rendered_json['results'][0]['primaryTitle'], self.film2.primaryTitle)

    def test_connected_actors(self):
        """Tests if the result films are listed with connected actors."""
        request = self.factory.get('/titles?startYear=1969')
        response = TitleList.as_view()(request)

        response.render()
        rendered_json = json.loads(response.content)
        self.assertEqual(rendered_json['results'][1]['name_set'][0]['primaryName'], self.name1.primaryName)

    def test_search_actors(self):
        """Tests if all films are listed for searched actor."""
        request = self.factory.get('/names?name=Fred Astaire')
        response = ActorTitleList.as_view()(request)

        response.render()
        rendered_json = json.loads(response.content)
        self.assertEqual(rendered_json['results'][0]['knownForTitles'][0]['primaryTitle'], self.film1.primaryTitle)

