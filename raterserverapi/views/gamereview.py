from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterserverapi.models import Game, Player, PlayerReviews

class GameReview(ViewSet):
    def create(self, request):
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game'])
        try:
            review = PlayerReviews.objects.create(
                player=player,
                content=request.data["review"],
                game=game
            )
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerReviews
        fields = ('id', 'player', 'content', 'game')
        depth = 1
