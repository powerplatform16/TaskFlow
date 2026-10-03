from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Category, Task, Note


class TaskFlowModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Testing Category",
            color="indigo",
            icon="code"
        )
        self.task = Task.objects.create(
            title="Unit Test Task",
            description="Testing task description",
            category=self.category,
            priority="HIGH",
            status="PENDING",
            due_date=timezone.localdate() + timedelta(days=2),
            estimated_hours=2.5
        )

    def test_category_slug_generation(self):
        self.assertEqual(self.category.slug, "testing-category")

    def test_task_toggle_status(self):
        self.assertEqual(self.task.status, "PENDING")
        self.assertIsNone(self.task.completed_at)
        
        # Toggle to complete
        self.task.toggle_status()
        self.assertEqual(self.task.status, "COMPLETED")
        self.assertIsNotNone(self.task.completed_at)
        
        # Toggle back to pending
        self.task.toggle_status()
        self.assertEqual(self.task.status, "PENDING")
        self.assertIsNone(self.task.completed_at)

    def test_category_completion_metrics(self):
        self.assertEqual(self.category.total_tasks_count, 1)
        self.assertEqual(self.category.completed_tasks_count, 0)
        self.assertEqual(self.category.completion_rate, 0)

        self.task.status = "COMPLETED"
        self.task.save()

        self.assertEqual(self.category.completed_tasks_count, 1)
        self.assertEqual(self.category.completion_rate, 100)


class TaskFlowViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Dev", color="blue")
        self.task = Task.objects.create(
            title="Initial Test Task",
            category=self.category,
            priority="URGENT",
            status="PENDING"
        )

    def test_dashboard_view_status_code(self):
        response = self.client.get(reverse('tasks:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/dashboard.html')
        self.assertContains(response, "Initial Test Task")

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertEqual(len(response.context['tasks']), 1)

    def test_task_create_view(self):
        response = self.client.post(reverse('tasks:task_create'), {
            'title': 'Newly Created Task',
            'description': 'Description content',
            'priority': 'MEDIUM',
            'status': 'PENDING',
            'estimated_hours': 1.5
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Task.objects.filter(title='Newly Created Task').exists())

    def test_task_toggle_status_view(self):
        response = self.client.post(reverse('tasks:task_toggle', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'COMPLETED')

    def test_export_csv_view(self):
        response = self.client.get(reverse('tasks:export_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Initial Test Task', response.content.decode('utf-8'))

    def test_export_json_view(self):
        response = self.client.get(reverse('tasks:export_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('Initial Test Task', response.content.decode('utf-8'))
