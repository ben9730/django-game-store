from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Game, Platform, GameImage, GameVideo
from .forms import GameImageForm, GameVideoForm


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    paginate_by = 20

    def get_queryset(self):
        queryset = Game.objects.all()
        platform = self.request.GET.get('platform')
        
        if platform:
            queryset = queryset.filter(platforms__name=platform)
        
        return queryset


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        context['videos'] = self.object.videos.all()
        return context





class PlatformListView(ListView):
    model = Platform
    template_name = 'games/platform_list.html'
    context_object_name = 'platforms'


class PlatformDetailView(DetailView):
    model = Platform
    template_name = 'games/platform_detail.html'
    context_object_name = 'platform'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platforms'] = Platform.objects.all()
        return context


class GameImageUploadView(View):
    def get(self, request, pk):
        game = get_object_or_404(Game, id=pk)
        images = game.images.all()
        return render(request, 'games/game_image_upload.html', {
            'game': game,
            'images': images,
            'form': GameImageForm()
        })

    def post(self, request, pk):
        game = get_object_or_404(Game, id=pk)
        form = GameImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.game = game
            image.save()
            messages.success(request, 'Image uploaded successfully')
            return redirect('games:game_image_upload', pk=pk)
        return render(request, 'games/game_image_upload.html', {
            'game': game,
            'form': form
        })

class GameImageDeleteView(View):
    def post(self, request, pk, image_id):
        image = get_object_or_404(GameImage, id=image_id)
        image.delete()
        return redirect('games:game_image_upload', pk=pk)


class GameVideoUploadView(View):
    def get(self, request, pk):
        game = get_object_or_404(Game, id=pk)
        videos = game.videos.all()
        return render(request, 'games/game_video_upload.html', {
            'game': game,
            'videos': videos,
            'form': GameVideoForm()
        })

    def post(self, request, pk):
        game = get_object_or_404(Game, id=pk)
        form = GameVideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.game = game
            video.save()
            messages.success(request, 'Video added successfully')
            return redirect('games:game_video_upload', pk=pk)
        return render(request, 'games/game_video_upload.html', {
            'game': game,
            'form': form
        })

class GameVideoDeleteView(View):
    def get(self, request, pk, video_id):
        video = get_object_or_404(GameVideo, id=video_id)
        video.delete()
        messages.success(request, 'Video deleted successfully')
        return redirect('games:game_video_upload', pk=pk)


@method_decorator(staff_member_required, name='dispatch')
class GameDeleteView(View):
    """Allow staff to delete a game."""
    def post(self, request, pk):
        game = get_object_or_404(Game, id=pk)
        game.delete()
        messages.success(request, 'Game deleted successfully')
        return redirect('games:game_list')
        return redirect('games:game_video_upload', pk=pk)
