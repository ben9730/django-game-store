from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Game, Platform, GameImage, GameVideo
from .forms import GameImageForm, GameVideoForm, PlatformForm


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    paginate_by = 20

    def get_queryset(self):
        return Game.objects.all()


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
        context['games'] = self.object.game_set.all()
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


# ------------------- Platform Create / Update -------------------
@method_decorator(staff_member_required, name='dispatch')
class PlatformCreateView(View):
    """Allow staff users to add a new gaming platform."""

    def get(self, request):
        form = PlatformForm()
        return render(request, 'games/platform_form.html', {'form': form})

    def post(self, request):
        form = PlatformForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Platform added successfully')
            return redirect('games:platform_list')
        return render(request, 'games/platform_form.html', {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class PlatformUpdateView(View):
    """Allow staff users to edit an existing platform."""

    def get(self, request, pk):
        platform = get_object_or_404(Platform, id=pk)
        form = PlatformForm(instance=platform)
        return render(request, 'games/platform_form.html', {'form': form, 'platform': platform})

    def post(self, request, pk):
        platform = get_object_or_404(Platform, id=pk)
        form = PlatformForm(request.POST, instance=platform)
        if form.is_valid():
            form.save()
            messages.success(request, 'Platform updated successfully')
            return redirect('games:platform_list')
        return render(request, 'games/platform_form.html', {'form': form, 'platform': platform})
        return redirect('games:game_video_upload', pk=pk)


############################
# Cart helpers and views   #
############################

def _get_cart(user):
    """Return existing cart for user or create a new one."""
    from .models import Cart  # local import to avoid circular
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    """Add a game to the authenticated user's cart."""
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        cart = _get_cart(request.user)
        item, created = cart.items.get_or_create(game=game, defaults={'price': game.price})
        if not created:
            item.quantity += 1
            item.save()
        messages.success(request, f'"{game.title}" added to your cart')
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('games:cart_detail')
        return HttpResponseRedirect(next_url)


@method_decorator(login_required, name='dispatch')
class CartDetailView(DetailView):
    template_name = 'games/cart_detail.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        return _get_cart(self.request.user)


@method_decorator(login_required, name='dispatch')
class RemoveCartItemView(View):
    def post(self, request, item_id):
        from .models import CartItem
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        messages.info(request, 'Item removed from cart')
        return redirect('games:cart_detail')


@method_decorator(login_required, name='dispatch')
class CartCheckoutView(View):
    """Convert cart items into purchased games (UserGame) and clear cart."""
    def post(self, request):
        from users.models import UserGame
        cart = _get_cart(request.user)
        if not cart.items.exists():
            messages.warning(request, 'Your cart is empty.')
            return redirect('games:cart_detail')
        for item in cart.items.select_related('game'):
            UserGame.objects.get_or_create(user_id=request.user.id, game=item.game)
        cart.items.all().delete()
        messages.success(request, 'Purchase successful! Games added to your library.')
        return redirect('users:library')
