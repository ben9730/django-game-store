from rest_framework import serializers
from ..models import Game, Platform, GameImage, GameVideo


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name', 'description']



class GameImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameImage
        fields = ['id', 'image', 'is_main']


class GameVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameVideo
        fields = ['id', 'video_url', 'title']


class GameSerializer(serializers.ModelSerializer):
    platforms = PlatformSerializer(many=True)
    images = GameImageSerializer(many=True)
    videos = GameVideoSerializer(many=True)

    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'price', 'platforms', 'status', 'release_date', 'download_link', 'image_url', 'images', 'videos']

    def create(self, validated_data):
        platforms_data = validated_data.pop('platforms')
        images_data = validated_data.pop('images', [])
        videos_data = validated_data.pop('videos', [])

        # Create or get category
        category, _ = Category.objects.get_or_create(**category_data)
        
        # Create game
        game = Game.objects.create(category=category, **validated_data)
        
        # Add platforms
        for platform_data in platforms_data:
            platform, _ = Platform.objects.get_or_create(**platform_data)
            game.platforms.add(platform)
        
        # Add images
        for image_data in images_data:
            GameImage.objects.create(game=game, **image_data)
        
        # Add videos
        for video_data in videos_data:
            GameVideo.objects.create(game=game, **video_data)
        
        return game

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        platforms_data = validated_data.pop('platforms', [])
        images_data = validated_data.pop('images', [])
        videos_data = validated_data.pop('videos', [])

        # Update game fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update category if provided
        if category_data:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.category = category
        
        # Update platforms
        instance.platforms.clear()
        for platform_data in platforms_data:
            platform, _ = Platform.objects.get_or_create(**platform_data)
            instance.platforms.add(platform)
        
        # Update images
        instance.images.all().delete()
        for image_data in images_data:
            GameImage.objects.create(game=instance, **image_data)
        
        # Update videos
        instance.videos.all().delete()
        for video_data in videos_data:
            GameVideo.objects.create(game=instance, **video_data)
        
        instance.save()
        return instance
