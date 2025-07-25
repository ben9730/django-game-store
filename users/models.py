from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Additional user fields
    is_subscribed = models.BooleanField(default=False)
    subscription_end_date = models.DateField(null=True, blank=True)

    # Override related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class UserGame(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_games')
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    last_played = models.DateTimeField(null=True, blank=True)
    play_time = models.DurationField(default=0)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"
