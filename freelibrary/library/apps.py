from django.apps import AppConfig


class LibraryConfig(AppConfig):
    verbose_name = 'Книги'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
