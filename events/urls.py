from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Dashboard / home
    path('', views.DashboardView.as_view(), name='dashboard'),

    # Category CRUD
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-add'),


    # Participant CRUD
    path('participants/', views.ParticipantListView.as_view(), name='participant_list'),
    path('participants/add/', views.ParticipantListView.as_view(), name='participant_list'),
    path('participants/new/', views.ParticipantCreateView.as_view(), name='participant_create'),
    path('participants/<int:pk>/edit/', views.ParticipantUpdateView.as_view(), name='participant_update'),
    path('participants/<int:pk>/delete/', views.ParticipantDeleteView.as_view(), name='participant_delete'),
    path('participants/add/', views.ParticipantCreateView.as_view(), name='participant-add'),


    # Event CRUD & detail
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/new/', views.EventListView.as_view(), name='event_list'),
    path('events/new/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    # JSON endpoints for interactive stats
    path('api/stats/', views.stats_api, name='api_stats'),
]
