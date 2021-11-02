from django.db import models

class Pictures(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=40)
