from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Game, Platform
from .serializers import GameSerializer, PlatformSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platforms', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price', 'release_date']

    def get_queryset(self):
        queryset = Game.objects.all()
        platform = self.request.query_params.get('platform')
        
        if platform:
            queryset = queryset.filter(platforms__name=platform)
        
        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured games"""
        featured_games = Game.objects.filter(status='available').order_by('-release_date')[:10]
        serializer = self.get_serializer(featured_games, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        game = self.get_object()
        related_games = Game.objects.filter(
            platforms__in=game.platforms.all()
        ).exclude(pk=game.pk)[:4]
        serializer = self.get_serializer(related_games, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """Upload an image to a game"""
        game = self.get_object()
        if 'image' not in request.data:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

        image = request.data['image']
        game.image_url = image.url if hasattr(image, 'url') else image
        game.save()
        return Response({'message': 'Image uploaded successfully'})

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get recommended games based on user's platform preferences"""
        user_platforms = request.user.profile.preferred_platforms.all()
        if user_platforms.exists():
            recommended_games = Game.objects.filter(
                platforms__in=user_platforms,
                status='available'
            ).distinct().order_by('-release_date')[:10]
        else:
            recommended_games = Game.objects.filter(status='available').order_by('-release_date')[:10]
        serializer = self.get_serializer(recommended_games, many=True)
        return Response(serializer.data)



    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
