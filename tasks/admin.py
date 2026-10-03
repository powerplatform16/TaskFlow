from django.contrib import admin
from .models import Category, Task, Note


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'icon', 'total_tasks_count', 'completed_tasks_count', 'completion_rate', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('color', 'created_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status', 'due_date', 'estimated_hours', 'completed_at', 'created_at')
    list_filter = ('status', 'priority', 'category', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'
    list_editable = ('status', 'priority')
    actions = ['mark_completed', 'mark_pending']

    @admin.action(description="Mark selected tasks as Completed")
    def mark_completed(self, request, queryset):
        queryset.update(status='COMPLETED')

    @admin.action(description="Mark selected tasks as Pending")
    def mark_pending(self, request, queryset):
        queryset.update(status='PENDING', completed_at=None)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_pinned', 'theme', 'updated_at', 'created_at')
    list_filter = ('is_pinned', 'theme', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_pinned',)
