from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    designer = models.CharField(max_length=40)
    number_of_players = models.IntegerField()
    time_to_play = models.FloatField()
    age_recommendation = models.IntegerField()
    release_year = models.IntegerField()