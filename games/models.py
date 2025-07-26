from django.db import models
from django.urls import reverse
from django.conf import settings


class Platform(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    platforms = models.ManyToManyField('Platform')
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('coming_soon', 'Coming Soon')
    ], default='published')
    image_url = models.URLField(blank=True, null=True)
    download_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game_detail', args=[str(self.id)])

    def get_image_url(self):
        """Return the first associated image URL or empty string."""
        if self.images.exists():
            return self.images.first().image_url or ''
        return ''

    def get_video_urls(self):
        return [video.video_url for video in self.videos.all()]


class GameImage(models.Model):
    game = models.ForeignKey(Game, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)
    is_main_image = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.game.title} - Image {self.id}"

    def get_image_url(self):
        return self.image_url


class GameVideo(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField()
    title = models.CharField(max_length=200, blank=True, null=True)
    is_main_video = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.game.title} - {self.title}"


class Cart(models.Model):
    """Shopping cart linked to a user."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.id} for {self.user.username}"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('cart', 'game')

    def __str__(self):
        return f"{self.game.title} x{self.quantity}"

    def subtotal(self):
        return self.price * self.quantity
