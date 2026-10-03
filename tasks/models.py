from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    COLOR_CHOICES = [
        ('indigo', 'Indigo (#6366F1)'),
        ('blue', 'Blue (#3B82F6)'),
        ('emerald', 'Emerald (#10B981)'),
        ('amber', 'Amber (#F59E0B)'),
        ('rose', 'Rose (#F43F5E)'),
        ('purple', 'Purple (#A855F7)'),
        ('cyan', 'Cyan (#06B6D4)'),
        ('gray', 'Slate (#64748B)'),
    ]

    ICON_CHOICES = [
        ('briefcase', 'Briefcase (Work)'),
        ('user', 'User (Personal)'),
        ('academic-cap', 'Graduation Cap (Study/Learning)'),
        ('currency-dollar', 'Currency (Finance)'),
        ('heart', 'Heart (Health & Fitness)'),
        ('code', 'Code (Development)'),
        ('sparkles', 'Sparkles (Ideas)'),
        ('folder', 'Folder (General)'),
    ]

    name = models.CharField(max_length=100, unique=True, help_text="Category name, e.g. Work, Personal")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Optional brief description")
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='indigo')
    icon = models.CharField(max_length=30, choices=ICON_CHOICES, default='folder')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tasks:task_list') + f'?category={self.slug}'

    @property
    def total_tasks_count(self):
        return self.tasks.count()

    @property
    def completed_tasks_count(self):
        return self.tasks.filter(status='COMPLETED').count()

    @property
    def completion_rate(self):
        total = self.total_tasks_count
        if total == 0:
            return 0
        return int((self.completed_tasks_count / total) * 100)


class TaskQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status='PENDING')

    def in_progress(self):
        return self.filter(status='IN_PROGRESS')

    def completed(self):
        return self.filter(status='COMPLETED')

    def active(self):
        return self.exclude(status__in=['COMPLETED', 'ARCHIVED'])

    def due_today(self):
        today = timezone.localdate()
        return self.filter(due_date=today).exclude(status='COMPLETED')

    def overdue(self):
        today = timezone.localdate()
        return self.filter(due_date__lt=today).exclude(status='COMPLETED')

    def search(self, query):
        if not query:
            return self
        return self.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(category__name__icontains=query)
        )


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ARCHIVED', 'Archived'),
    ]

    title = models.CharField(max_length=200, help_text="Clear title of the task")
    description = models.TextField(blank=True, help_text="Detailed notes or checklists")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    due_date = models.DateField(null=True, blank=True, help_text="Target completion date")
    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0.0,
        help_text="Estimated time in hours (e.g. 1.5)"
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaskQuerySet.as_manager()

    class Meta:
        ordering = ['-priority', 'due_date', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.pk})

    def toggle_status(self):
        """Helper to quickly switch between completed and pending."""
        if self.status == 'COMPLETED':
            self.status = 'PENDING'
            self.completed_at = None
        else:
            self.status = 'COMPLETED'
            self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at', 'updated_at'])

    @property
    def is_overdue(self):
        if self.due_date and self.status != 'COMPLETED':
            return self.due_date < timezone.localdate()
        return False

    @property
    def is_due_today(self):
        if self.due_date and self.status != 'COMPLETED':
            return self.due_date == timezone.localdate()
        return False

    @property
    def priority_badge(self):
        badges = {
            'LOW': {'bg': 'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200 border-slate-200', 'dot': 'bg-slate-400'},
            'MEDIUM': {'bg': 'bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-200 border-blue-200', 'dot': 'bg-blue-500'},
            'HIGH': {'bg': 'bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-200 border-amber-200', 'dot': 'bg-amber-500'},
            'URGENT': {'bg': 'bg-rose-100 text-rose-800 dark:bg-rose-900/60 dark:text-rose-200 border-rose-200', 'dot': 'bg-rose-500'},
        }
        return badges.get(self.priority, badges['MEDIUM'])

    @property
    def status_badge(self):
        badges = {
            'PENDING': {'bg': 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300', 'icon': 'clock'},
            'IN_PROGRESS': {'bg': 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/60 dark:text-indigo-200', 'icon': 'play'},
            'COMPLETED': {'bg': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-200', 'icon': 'check-circle'},
            'ARCHIVED': {'bg': 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400', 'icon': 'archive'},
        }
        return badges.get(self.status, badges['PENDING'])


class Note(models.Model):
    THEME_CHOICES = [
        ('yellow', 'Warm Amber'),
        ('blue', 'Sky Blue'),
        ('emerald', 'Emerald Mint'),
        ('purple', 'Purple Lavender'),
        ('rose', 'Rose Bloom'),
        ('slate', 'Modern Slate'),
    ]

    title = models.CharField(max_length=200, help_text="Note headline")
    content = models.TextField(help_text="Body content or bullet points")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notes'
    )
    is_pinned = models.BooleanField(default=False, help_text="Pin to top of the dashboard and notes list")
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='yellow')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:note_list')
