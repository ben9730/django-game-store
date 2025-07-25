from django import forms
from games.models import Game, GameImage, GameVideo

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'price', 'status', 'release_date', 'platforms', 'download_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'platforms': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'download_link': forms.URLInput(attrs={'class': 'form-control'}),
        }

class GameImageForm(forms.ModelForm):
    class Meta:
        model = GameImage
        fields = ['image_url']
        widgets = {
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class GameVideoForm(forms.ModelForm):
    class Meta:
        model = GameVideo
        fields = ['video_url']
        widgets = {
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
