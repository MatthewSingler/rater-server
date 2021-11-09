from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterserverapi.models import Game, Player

class GameView(ViewSet):

    def create(self, request):
        """Handle POST operations
        """
        player = Player.objects.get(user=request.auth.user)
        try:
            game = Game.objects.create(
                title=request.data["title"],
                description=request.data["description"],
                designer=request.data["designer"],
                number_of_players=request.data["numberOfPlayers"],
                time_to_play=request.data["timeToPlay"],
                age_recommendation=request.data["ageRecommendation"],
                release_year=request.data["releaseYear"]
            )
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game
        """
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.time_to_play = request.data["timeToPlay"]
        game.age_recommendation = request.data["ageRecommendation"]
        game.release_year = request.data["releaseYear"]
        game.player = player
        game.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource
        """
        games = Game.objects.all()
        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type__id=game_type)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'number_of_players',
                  'time_to_play', 'age_recommendation', 'release_year')
        depth = 1
