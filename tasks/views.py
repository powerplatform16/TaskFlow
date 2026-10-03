import csv
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q

from .models import Task, Category, Note
from .forms import TaskForm, CategoryForm, NoteForm


class DashboardView(TemplateView):
    template_name = 'tasks/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        # Task Metrics
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='COMPLETED').count()
        in_progress_tasks = Task.objects.filter(status='IN_PROGRESS').count()
        pending_tasks = Task.objects.filter(status='PENDING').count()
        overdue_tasks = Task.objects.overdue().count()
        due_today_tasks = Task.objects.due_today().count()

        completion_rate = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

        # Highlights
        urgent_tasks = Task.objects.filter(
            priority__in=['HIGH', 'URGENT']
        ).exclude(status='COMPLETED').order_by('due_date', '-priority')[:5]

        tasks_due_today = Task.objects.due_today()[:5]
        recent_tasks = Task.objects.select_related('category').order_by('-created_at')[:6]
        pinned_notes = Note.objects.filter(is_pinned=True)[:4]
        recent_notes = Note.objects.all()[:4]
        categories = Category.objects.annotate(
            total_count=Count('tasks'),
            completed_count=Count('tasks', filter=Q(tasks__status='COMPLETED'))
        ).order_by('-total_count')[:6]

        context.update({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'due_today_tasks': due_today_tasks,
            'completion_rate': completion_rate,
            'urgent_tasks': urgent_tasks,
            'tasks_due_today': tasks_due_today,
            'recent_tasks': recent_tasks,
            'pinned_notes': pinned_notes,
            'recent_notes': recent_notes,
            'categories': categories,
            'today': today,
        })
        return context


# ==========================================
# Task Views
# ==========================================

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        qs = Task.objects.select_related('category').all()

        # Filtering parameters
        q = self.request.GET.get('q', '').strip()
        category_slug = self.request.GET.get('category', '').strip()
        status = self.request.GET.get('status', '').strip()
        priority = self.request.GET.get('priority', '').strip()
        filter_type = self.request.GET.get('filter', '').strip()
        sort_by = self.request.GET.get('sort', '-created_at').strip()

        if q:
            qs = qs.search(q)
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        
        # Quick preset filters
        if filter_type == 'due_today':
            qs = qs.due_today()
        elif filter_type == 'overdue':
            qs = qs.overdue()
        elif filter_type == 'completed':
            qs = qs.completed()
        elif filter_type == 'active':
            qs = qs.active()

        # Ordering
        valid_sorts = {
            'due_asc': 'due_date',
            'due_desc': '-due_date',
            'priority_desc': '-priority',
            'priority_asc': 'priority',
            'newest': '-created_at',
            'oldest': 'created_at',
            'title_asc': 'title',
        }
        order_field = valid_sorts.get(sort_by, '-created_at')
        return qs.order_by(order_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_q'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['current_filter'] = self.request.GET.get('filter', '')
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        messages.success(self.request, f'Task "{form.instance.title}" created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Create New Task"
        context['btn_text'] = "Create Task"
        return context


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        messages.success(self.request, f'Task "{form.instance.title}" updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Edit Task"
        context['btn_text'] = "Save Changes"
        return context


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        messages.warning(request, f'Task "{task.title}" has been deleted.')
        return super().delete(request, *args, **kwargs)


class TaskToggleStatusView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.toggle_status()
        status_label = "completed" if task.status == 'COMPLETED' else "marked as pending"
        messages.success(request, f'Task "{task.title}" {status_label}!')
        
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('tasks:task_list')
        return redirect(next_url)


# ==========================================
# Category Views
# ==========================================

class CategoryListView(ListView):
    model = Category
    template_name = 'tasks/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(
            total_tasks=Count('tasks'),
            completed_tasks=Count('tasks', filter=Q(tasks__status='COMPLETED'))
        ).order_by('name')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('tasks:category_list')

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Create New Category"
        context['btn_text'] = "Create Category"
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('tasks:category_list')

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Edit Category"
        context['btn_text'] = "Save Changes"
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'tasks/category_confirm_delete.html'
    success_url = reverse_lazy('tasks:category_list')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.warning(request, f'Category "{category.name}" and references have been removed.')
        return super().delete(request, *args, **kwargs)


# ==========================================
# Note Views
# ==========================================

class NoteListView(ListView):
    model = Note
    template_name = 'tasks/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        qs = Note.objects.select_related('category').all()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_q'] = self.request.GET.get('q', '')
        return context


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'tasks/note_form.html'
    success_url = reverse_lazy('tasks:note_list')

    def form_valid(self, form):
        messages.success(self.request, f'Note "{form.instance.title}" added!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Create New Note"
        context['btn_text'] = "Create Note"
        return context


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'tasks/note_form.html'
    success_url = reverse_lazy('tasks:note_list')

    def form_valid(self, form):
        messages.success(self.request, f'Note "{form.instance.title}" updated!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Edit Note"
        context['btn_text'] = "Save Changes"
        return context


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'tasks/note_confirm_delete.html'
    success_url = reverse_lazy('tasks:note_list')

    def delete(self, request, *args, **kwargs):
        note = self.get_object()
        messages.warning(request, f'Note "{note.title}" deleted.')
        return super().delete(request, *args, **kwargs)


class NoteTogglePinView(View):
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        note.is_pinned = not note.is_pinned
        note.save(update_fields=['is_pinned', 'updated_at'])
        state = "pinned" if note.is_pinned else "unpinned"
        messages.info(request, f'Note "{note.title}" {state}!')
        
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('tasks:note_list')
        return redirect(next_url)


# ==========================================
# Data Export Views (Intermediate Django Feature)
# ==========================================

def export_tasks_csv(request):
    """Demonstrates generating dynamic CSV downloads directly in Django."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="taskflow_export_{timezone.localdate()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Category', 'Priority', 'Status', 'Due Date', 'Estimated Hours', 'Created At'])

    tasks = Task.objects.select_related('category').all().order_by('-created_at')
    for task in tasks:
        writer.writerow([
            task.id,
            task.title,
            task.category.name if task.category else 'None',
            task.priority,
            task.status,
            task.due_date.isoformat() if task.due_date else '',
            task.estimated_hours,
            task.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    return response


def export_tasks_json(request):
    """Demonstrates JSON serialization and data export."""
    tasks = Task.objects.select_related('category').all().order_by('-created_at')
    data = [
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'category': t.category.name if t.category else None,
            'priority': t.priority,
            'status': t.status,
            'due_date': t.due_date.isoformat() if t.due_date else None,
            'estimated_hours': float(t.estimated_hours),
            'created_at': t.created_at.isoformat(),
        }
        for t in tasks
    ]
    response = JsonResponse(data, safe=False, json_dumps_params={'indent': 2})
    response['Content-Disposition'] = f'attachment; filename="taskflow_export_{timezone.localdate()}.json"'
    return response


def seed_demo_data_view(request):
    """Allows user to populate demo sample tasks and notes in 1 click."""
    if request.method == 'POST':
        from .utils import populate_demo_data
        populate_demo_data()
        messages.success(request, "Sample tasks, categories, and notes have been populated successfully!")
        return redirect('tasks:dashboard')
    return redirect('tasks:dashboard')
