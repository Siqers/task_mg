import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.projects.models import Epic, Membership, Project, Sprint
from apps.tasks.models import Comment, SubTask, Tag, Task

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with demo SprintHub data.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Seeding SprintHub data...'))

        Comment.objects.all().delete()
        SubTask.objects.all().delete()
        Task.objects.all().delete()
        Tag.objects.all().delete()
        Membership.objects.all().delete()
        Epic.objects.all().delete()
        Sprint.objects.all().delete()
        Project.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        admin_user, created = User.objects.get_or_create(
            email='admin@spinthub.com',
            defaults={
                'full_name': 'SprintHub Admin',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        admin_user.set_password('admin123')
        admin_user.save()
        self.stdout.write(self.style.SUCCESS('Superuser ready: admin@spinthub.com / admin123'))

        user_payloads = [
            ('alina@spinthub.com', 'Alina Sarsenova'),
            ('daniyar@spinthub.com', 'Daniyar Bektas'),
            ('aigerim@spinthub.com', 'Aigerim Omarova'),
            ('nurbol@spinthub.com', 'Nurbol Serik'),
            ('madina@spinthub.com', 'Madina Toleu'),
            ('askar@spinthub.com', 'Askar Nurlan'),
            ('dias@spinthub.com', 'Dias Kairat'),
        ]

        users = []
        for index, (email, full_name) in enumerate(user_payloads, start=1):
            user = User.objects.create_user(
                email=email,
                full_name=full_name,
                phone=f'+770100000{index:02d}',
                password='password123',
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS('Created 7 regular users.'))

        project_data = [
            ('SprintHub Core Platform', 'Main API delivery for projects, tasks, comments, and authentication.'),
            ('Mobile Client Integration', 'Coordinate endpoints and delivery support for the mobile team.'),
            ('Analytics Workspace', 'Track reporting features, dashboards, and process improvements.'),
        ]

        projects = []
        for index, (name, description) in enumerate(project_data):
            owner = users[index]
            project = Project.objects.create(name=name, description=description, owner=owner)
            projects.append(project)

        membership_roles = [
            Membership.ROLE_CAPTAIN,
            Membership.ROLE_MEMBER,
            Membership.ROLE_MEMBER,
            Membership.ROLE_VIEWER,
        ]
        for project_index, project in enumerate(projects):
            sample_users = users[project_index:project_index + 4]
            for idx, member_user in enumerate(sample_users):
                Membership.objects.create(
                    user=member_user,
                    project=project,
                    role=membership_roles[idx % len(membership_roles)],
                )
        self.stdout.write(self.style.SUCCESS('Created 3 projects with memberships.'))

        today = date.today()
        sprints = []
        for project_index, project in enumerate(projects):
            for sprint_number in range(1, 3):
                start_date = today - timedelta(days=(project_index * 20) + sprint_number * 14)
                end_date = start_date + timedelta(days=13)
                sprint = Sprint.objects.create(
                    project=project,
                    title=f'{project.name} Sprint {sprint_number}',
                    start_date=start_date,
                    end_date=end_date,
                    is_active=sprint_number == 2,
                )
                sprints.append(sprint)
        self.stdout.write(self.style.SUCCESS('Created 6 sprints.'))

        epic_templates = [
            ('Authentication & Access', 'Registration, login, profile, and JWT flow.'),
            ('Project Delivery', 'Project, membership, and sprint management.'),
            ('Task Execution', 'Tasks, subtasks, comments, and tag workflows.'),
            ('Reporting & Cleanup', 'Filters, admin panel, and technical debt management.'),
            ('Mobile Support', 'Endpoint adjustments for mobile consumption.'),
            ('Release Readiness', 'Documentation, testing, and final polishing.'),
            ('Analytics Tasks', 'Operational metrics and reporting endpoints.'),
            ('Team Productivity', 'Improve assignment visibility and collaboration.'),
        ]
        epic_statuses = [Epic.STATUS_OPEN, Epic.STATUS_IN_PROGRESS, Epic.STATUS_CLOSED]
        epics = []
        for index, (title, description) in enumerate(epic_templates):
            project = projects[index % len(projects)]
            related_sprints = [sprint for sprint in sprints if sprint.project_id == project.id]
            epic = Epic.objects.create(
                project=project,
                sprint=random.choice(related_sprints),
                title=title,
                description=description,
                status=epic_statuses[index % len(epic_statuses)],
            )
            epics.append(epic)
        self.stdout.write(self.style.SUCCESS('Created 8 epics.'))

        tag_names = ['backend', 'frontend', 'bug', 'feature', 'urgent', 'research', 'documentation']
        tags = [Tag.objects.create(name=name) for name in tag_names]
        self.stdout.write(self.style.SUCCESS('Created 7 tags.'))

        task_statuses = [
            Task.STATUS_TODO,
            Task.STATUS_IN_PROGRESS,
            Task.STATUS_REVIEW,
            Task.STATUS_DONE,
        ]
        task_priorities = [
            Task.PRIORITY_LOW,
            Task.PRIORITY_MEDIUM,
            Task.PRIORITY_HIGH,
            Task.PRIORITY_CRITICAL,
        ]

        task_titles = [
            'Design custom user model',
            'Implement registration endpoint',
            'Implement login endpoint',
            'Build profile endpoint',
            'Create project serializer',
            'Add project permissions',
            'Implement sprint filters',
            'Implement epic filters',
            'Build task serializer',
            'Add task filtering',
            'Create task detail endpoint',
            'Implement subtask endpoint',
            'Implement comment endpoint',
            'Configure drf-spectacular',
            'Document authentication flow',
            'Optimize project queryset',
            'Optimize task queryset',
            'Register models in admin',
            'Prepare seed data command',
            'Add sample memberships',
            'Connect JWT refresh flow',
            'Write ERD draft',
            'Validate endpoint permissions',
            'Review PEP8 formatting',
            'Prepare defense demo data',
        ]

        tasks = []
        for index, title in enumerate(task_titles):
            project = projects[index % len(projects)]
            project_epics = [epic for epic in epics if epic.project_id == project.id]
            author = users[index % len(users)]
            assignee = users[(index + 2) % len(users)]
            task = Task.objects.create(
                project=project,
                epic=random.choice(project_epics),
                title=title,
                description=f'{title} for {project.name}. This task is part of the midterm delivery workflow.',
                status=task_statuses[index % len(task_statuses)],
                priority=task_priorities[index % len(task_priorities)],
                author=author,
                assignee=assignee,
                due_date=today + timedelta(days=(index % 10) + 1),
            )
            selected_tags = random.sample(tags, k=random.randint(1, 3))
            task.tags.set(selected_tags)
            tasks.append(task)
        self.stdout.write(self.style.SUCCESS('Created 25 tasks.'))

        subtask_templates = [
            'Draft implementation plan',
            'Write serializer',
            'Write view logic',
            'Test endpoint manually',
            'Record screen demo',
        ]
        created_subtasks = 0
        for index, task in enumerate(tasks):
            subtask_count = 2 if index < 10 else 1 if index < 15 else 2
            for sub_index in range(subtask_count):
                SubTask.objects.create(
                    task=task,
                    title=f'{subtask_templates[sub_index % len(subtask_templates)]} for {task.title}',
                    is_completed=(sub_index + index) % 3 == 0,
                )
                created_subtasks += 1
        while created_subtasks < 42:
            task = random.choice(tasks)
            SubTask.objects.create(
                task=task,
                title=f'Extra checklist item {created_subtasks + 1} for {task.title}',
                is_completed=created_subtasks % 2 == 0,
            )
            created_subtasks += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_subtasks} subtasks.'))

        comment_bodies = [
            'Please review this part before the daily standup.',
            'I updated the serializer and pushed the latest changes.',
            'Need to verify permissions for this flow.',
            'This is ready for QA and documentation screenshots.',
            'Let us keep this task in the current sprint.',
        ]
        created_comments = 0
        for index, task in enumerate(tasks[:20]):
            comment_total = 1 if index % 2 == 0 else 2
            for inner_index in range(comment_total):
                Comment.objects.create(
                    task=task,
                    author=users[(index + inner_index) % len(users)],
                    body=comment_bodies[(index + inner_index) % len(comment_bodies)],
                )
                created_comments += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_comments} comments.'))

        self.stdout.write(self.style.SUCCESS('Database successfully seeded with SprintHub demo data.'))
