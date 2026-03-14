# SprintHub API

SprintHub API is a Django REST Framework project for a task management system with projects, sprints, epics, tasks, subtasks, comments, tags, and user authentication.

The project was built for a MidTerm defense and includes:

- custom User model
- JWT authentication
- filtering
- custom permissions
- API documentation with drf-spectacular
- admin panel configuration
- seed command for filling the database with demo data

---

## Tech Stack

- Python 3.9+
- Django 4.2.7
- Django REST Framework 3.14.0
- djangorestframework-simplejwt 5.3.0
- drf-spectacular 0.26.5
- django-filter 23.3
- python-decouple 3.8

---

## Main Features

- Custom user model with **email** as the main authentication field
- JWT-based authentication
- Project management
- Sprint and Epic management
- Task management with priorities and statuses
- Subtasks and comments
- Tag system
- Filtering for tasks, sprints, and epics
- Custom permissions for projects, tasks, and comments
- Swagger/OpenAPI documentation
- Admin panel for all models
- Seed command to generate demo data

---

## Project Structure

```text
spinthub/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── __init__.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   │       └── __init__.py
│   ├── projects/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── filters.py
│   │   ├── permissions.py
│   │   └── migrations/
│   │       └── __init__.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── filters.py
│   │   ├── permissions.py
│   │   └── migrations/
│   │       └── __init__.py
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── seed_data.py