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
        
        # Process image forms
        for i in range(1, 6):  # Support up to 5 images
            if f'image_{i}' in request.FILES or f'image_url_{i}' in request.POST:
                image_forms.append(GameImageForm({
                    'image': request.FILES.get(f'image_{i}'),
                    'image_url': request.POST.get(f'image_url_{i}')
                }))
        
        # Process video forms
        for i in range(1, 3):  # Support up to 2 videos
            if f'video_url_{i}' in request.POST:
                video_forms.append(GameVideoForm({
                    'video_url': request.POST.get(f'video_url_{i}')
                }))
        
        if game_form.is_valid() and all(form.is_valid() for form in image_forms) and all(form.is_valid() for form in video_forms):
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
