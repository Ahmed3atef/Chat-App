import pytest
from django.conf import settings as django_settings


@pytest.fixture(scope='session', autouse=True)
def setup_test_settings():
    """Configure Django settings for tests"""
    # Force use of StaticFilesStorage instead of ManifestStaticFilesStorage
    django_settings.STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # Enable DEBUG mode for tests to avoid static file issues
    django_settings.DEBUG = True


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    """Use temporary directory for media files during tests"""
    settings.MEDIA_ROOT = tmpdir.strpath
