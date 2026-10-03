from django import forms
from .models import Task, Category, Note


TAILWIND_INPUT_CLASS = (
    "w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 "
    "bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 "
    "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 "
    "transition duration-150 shadow-sm text-sm"
)

TAILWIND_SELECT_CLASS = (
    "w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 "
    "bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 "
    "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 "
    "transition duration-150 shadow-sm text-sm"
)

TAILWIND_TEXTAREA_CLASS = (
    "w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 "
    "bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 "
    "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 "
    "transition duration-150 shadow-sm text-sm resize-y"
)

TAILWIND_CHECKBOX_CLASS = (
    "h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded dark:bg-slate-900 dark:border-slate-700"
)


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': TAILWIND_INPUT_CLASS,
            }
        )
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'status', 'due_date', 'estimated_hours']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Design homepage layout or Review weekly budget',
                'class': TAILWIND_INPUT_CLASS
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Add checklists, steps, or important context...',
                'class': TAILWIND_TEXTAREA_CLASS
            }),
            'category': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS
            }),
            'priority': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS
            }),
            'status': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS
            }),
            'estimated_hours': forms.NumberInput(attrs={
                'step': '0.5',
                'min': '0',
                'placeholder': '0.0',
                'class': TAILWIND_INPUT_CLASS
            }),
        }

    def clean_estimated_hours(self):
        hours = self.cleaned_data.get('estimated_hours')
        if hours is not None and hours < 0:
            raise forms.ValidationError("Estimated hours cannot be negative.")
        return hours


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color', 'icon', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Work, Health, Personal Projects',
                'class': TAILWIND_INPUT_CLASS
            }),
            'color': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS
            }),
            'icon': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Brief description of this category (optional)...',
                'class': TAILWIND_TEXTAREA_CLASS
            }),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'theme', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Ideas for sprint retrospective',
                'class': TAILWIND_INPUT_CLASS
            }),
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Type your thoughts, quick snippets, or meeting minutes...',
                'class': TAILWIND_TEXTAREA_CLASS
            }),
            'category': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS
            }),
            'theme': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': TAILWIND_CHECKBOX_CLASS
            }),
        }
