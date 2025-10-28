

# Create your views here.
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import date

from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

# Category views
class CategoryListView(generic.ListView):
    model = Category
    template_name = 'events/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/category_form.html'
    success_url = reverse_lazy('events:category_list')


class CategoryUpdateView(generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/category_form.html'
    success_url = reverse_lazy('events:category_list')


class CategoryDeleteView(generic.DeleteView):
    model = Category
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('events:category_list')


# Participant views
class ParticipantListView(generic.ListView):
    model = Participant
    template_name = 'events/participant_list.html'
    context_object_name = 'participants'


class ParticipantCreateView(generic.CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'events/participant_form.html'
    success_url = reverse_lazy('events:participant_list')


class ParticipantUpdateView(generic.UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'events/participant_form.html'
    success_url = reverse_lazy('events:participant_list')


class ParticipantDeleteView(generic.DeleteView):
    model = Participant
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('events:participant_list')


# Event views with optimized queries, search, filter, aggregation
class EventListView(generic.ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 15

    def get_queryset(self):
        qs = Event.objects.all().select_related('category').prefetch_related('participants').annotate(
            participant_count=Count('participants')
        )
        # search
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(location__icontains=q))

        # filter by category
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__id=category)

        # filter by date range
        start = self.request.GET.get('start_date')
        end = self.request.GET.get('end_date')
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # aggregate: total participants across all events
        total_participants = Event.objects.aggregate(total=Count('participants'))['total']
        ctx['total_participants'] = total_participants or 0
        ctx['categories'] = Category.objects.all()
        # pass search params back to the template for UI
        ctx['q'] = self.request.GET.get('q', '')
        ctx['start_date'] = self.request.GET.get('start_date', '')
        ctx['end_date'] = self.request.GET.get('end_date', '')
        ctx['selected_category'] = self.request.GET.get('category', '')
        return ctx


class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        # ensure category and participants are loaded efficiently
        return Event.objects.select_related('category').prefetch_related('participants')


class EventCreateView(generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')


class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')


class EventDeleteView(generic.DeleteView):
    model = Event
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('events:event_list')


# Dashboard view with stats & today's events
class DashboardView(generic.TemplateView):
    template_name = 'events/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        total_participants = Event.objects.aggregate(total=Count('participants'))['total'] or 0
        total_events = Event.objects.count()
        upcoming_events = Event.objects.filter(date__gt=today).count()
        past_events = Event.objects.filter(date__lt=today).count()

        ctx.update({
            'total_participants': total_participants,
            'total_events': total_events,
            'upcoming_events': upcoming_events,
            'past_events': past_events,
            'todays_events': Event.objects.filter(date=today).select_related('category').prefetch_related('participants'),
        })
        return ctx

# Simple JSON API for interactive stats
def stats_api(request):
    """Return stats depending on query param 'type' = total | upcoming | past"""
    stype = request.GET.get('type', 'total')
    today = date.today()

    if stype == 'upcoming':
        qs = Event.objects.filter(date__gt=today)
    elif stype == 'past':
        qs = Event.objects.filter(date__lt=today)
    else:
        qs = Event.objects.all()

    # include counts and some sample events
    data = {
        'count': qs.count(),
        'events': list(qs.order_by('date').values('id', 'name', 'date', 'time', 'location')[:10])
    }
    return JsonResponse(data)
