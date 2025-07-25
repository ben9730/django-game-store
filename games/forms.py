from django import forms
from .models import Game, GameImage, GameVideo

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'price', 'release_date', 'status', 'download_link', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'download_link': forms.URLInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class GameImageForm(forms.ModelForm):
    class Meta:
        model = GameImage
        fields = ['image_url', 'is_main_image']
        widgets = {
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_main_image': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')
        
        if not image and not image_url:
            raise forms.ValidationError("Please provide either an image file or an image URL")
        
        return cleaned_data

class GameVideoForm(forms.ModelForm):
    class Meta:
        model = GameVideo
        fields = ['video_url', 'title', 'is_main_video']
        widgets = {
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_main_video': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        video_url = cleaned_data.get('video_url')
        if not video_url:
            raise forms.ValidationError("Please provide a video URL")
        return cleaned_data
