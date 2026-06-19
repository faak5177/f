import pytest
from django.conf import settings


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """
    Переопределяем настройку БД для тестов:
    используем реальную БД Demoekzamen без создания test_Demoekzamen.
    """
    settings.DATABASES['default'] = {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     'Demoekzamen',
        'USER':     'postgres',
        'PASSWORD': '123',
        'HOST':     'localhost',
        'PORT':     '5432',
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT':      True,
    }


@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    """Блокирует переименование БД в test_*."""
    pass
