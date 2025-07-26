from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.GameListView.as_view(), name='game_list'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('<int:pk>/images/', views.GameImageUploadView.as_view(), name='game_image_upload'),
    path('<int:pk>/images/<int:image_id>/delete/', views.GameImageDeleteView.as_view(), name='game_image_delete'),
    path('<int:pk>/videos/', views.GameVideoUploadView.as_view(), name='game_video_upload'),
    path('<int:pk>/videos/<int:video_id>/delete/', views.GameVideoDeleteView.as_view(), name='game_video_delete'),
    path('<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
    path('platforms/', views.PlatformListView.as_view(), name='platform_list'),
    path('platforms/add/', views.PlatformCreateView.as_view(), name='platform_add'),
    path('platforms/<int:pk>/edit/', views.PlatformUpdateView.as_view(), name='platform_edit'),
    path('platforms/<int:pk>/', views.PlatformDetailView.as_view(), name='platform_detail'),

    # Cart URLs
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:game_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.RemoveCartItemView.as_view(), name='remove_cart_item'),
    path('cart/checkout/', views.CartCheckoutView.as_view(), name='cart_checkout'),
]
