from django.db import models
from django.db.models.deletion import CASCADE

class PlayerReviews(models.Model):
    player = models.ForeignKey("Player", on_delete=CASCADE)
    content = models.CharField(max_length=40)
    game = models.ForeignKey("Game", on_delete=CASCADE)