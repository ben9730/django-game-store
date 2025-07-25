from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime
from .models import SalesReport
from games.models import Game, GameImage, GameVideo
from .forms import GameForm, GameImageForm, GameVideoForm

@staff_member_required
def admin_panel(request):
    if request.method == 'POST':
        game_form = GameForm(request.POST, request.FILES)
        image_forms = []
        video_forms = []
        
        # Process main image form (the first one displayed)
        main_image_form = GameImageForm(request.POST)
        if main_image_form.is_valid() and main_image_form.cleaned_data.get('image_url'):
            image_forms.append(main_image_form)
        
        # Process main video form (the first one displayed)
        main_video_form = GameVideoForm(request.POST)
        if main_video_form.is_valid() and main_video_form.cleaned_data.get('video_url'):
            video_forms.append(main_video_form)
        
        # Process additional image forms (dynamically added)
        for i in range(0, 10):  # Support up to 10 additional images
            if f'image_url_{i}' in request.POST and request.POST.get(f'image_url_{i}').strip():
                image_data = {'image_url': request.POST.get(f'image_url_{i}')}
                image_form = GameImageForm(image_data)
                if image_form.is_valid():
                    image_forms.append(image_form)
        
        # Process additional video forms (dynamically added)
        for i in range(0, 10):  # Support up to 10 additional videos
            if f'video_url_{i}' in request.POST and request.POST.get(f'video_url_{i}').strip():
                video_data = {
                    'video_url': request.POST.get(f'video_url_{i}'),
                    'title': request.POST.get(f'video_title_{i}', f'Video {i+1}')
                }
                video_form = GameVideoForm(video_data)
                if video_form.is_valid():
                    video_forms.append(video_form)
        
        if game_form.is_valid():
            game = game_form.save()
            
            # Save images
            for form in image_forms:
                image = form.save(commit=False)
                image.game = game
                image.save()
            
            # Save videos
            for form in video_forms:
                video = form.save(commit=False)
                video.game = game
                video.save()
            
            return redirect('admin_panel:admin_panel')
    else:
        game_form = GameForm()
        image_form = GameImageForm()
        video_form = GameVideoForm()
    
    context = {
        'game_form': game_form,
        'image_form': image_form,
        'video_form': video_form
    }
    return render(request, 'admin_panel/base_site.html', context)

@staff_member_required
def monthly_report(request, year, month):
    # Filter reports by month
    reports = SalesReport.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('-date')
    
    # Calculate monthly totals
    monthly_revenue = reports.aggregate(Sum('total_sales'))['total_sales__sum'] or 0
    monthly_orders = reports.aggregate(Count('id'))['id__count']
    
    # Get most sold games for this month
    most_sold_games = Game.objects.filter(
        salesreport__date__year=year,
        salesreport__date__month=month
    ).annotate(
        monthly_sales=Count('salesreport__id')
    ).order_by('-monthly_sales')[:5]
    
    context = {
        'reports': reports,
        'monthly_revenue': monthly_revenue,
        'monthly_orders': monthly_orders,
        'most_sold_games': most_sold_games,
        'year': year,
        'month': month
    }
    return render(request, 'admin_panel/monthly_report.html', context)
