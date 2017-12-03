from django.contrib.postgres.fields import ArrayField
from django.db import models


class Title(models.Model):
    """Model for title.basics db."""
    tconst = models.CharField(db_index=True, max_length=1024)
    titleType = models.CharField(max_length=1024)
    primaryTitle = models.CharField(max_length=1024)
    originalTitle = models.CharField(max_length=1024, null=True)
    isAdult = models.BooleanField(default=False)
    startYear = models.SmallIntegerField(db_index=True, null=True)
    endYear = models.SmallIntegerField(null=True)
    runtimeMinutes = models.DurationField(null=True)
    genres = ArrayField(models.CharField(max_length=32), default=[], db_index=True)


class Name(models.Model):
    """Model for name.basics db."""
    nconst = models.CharField(max_length=1024)
    primaryName = models.CharField(max_length=1024)
    birthYear = models.SmallIntegerField(null=True)
    deathYear = models.SmallIntegerField(null=True)
    primaryProfession = ArrayField(models.CharField(max_length=1024), default=[])
    knownForTitles = models.ManyToManyField(Title, through='KnownFor')


class KnownFor(models.Model):
    """Model for join table."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    name = models.ForeignKey(Name, on_delete=models.CASCADE)
