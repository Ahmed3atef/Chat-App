import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()


@pytest.fixture(autouse=True)
def mock_static_storage(settings):
    """Mock static storage to avoid manifest issues"""
    settings.STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    settings.DEBUG = True


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(client, user):
    """Return an authenticated client"""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.mark.django_db
class TestUserProfileApp:
    """Simple integration tests to verify the profile app works"""

    def test_user_can_view_own_profile(self, authenticated_client):
        """Test that a user can view their own profile"""
        response = authenticated_client.get(reverse('profile'))
        assert response.status_code == 200

    def test_user_can_access_profile_edit(self, authenticated_client):
        """Test that a user can access the profile edit page"""
        response = authenticated_client.get(reverse('profile-edit'))
        assert response.status_code == 200

    def test_user_can_update_profile(self, authenticated_client, user):
        """Test that a user can update their profile information"""
        response = authenticated_client.post(reverse('profile-edit'), {
            'displayname': 'New Name',
            'info': 'New bio'
        })
        assert response.status_code == 302  # Redirect after success

        user.profile.refresh_from_db()
        assert user.profile.displayname == 'New Name'

    def test_user_can_access_settings(self, authenticated_client):
        """Test that a user can access their settings page"""
        response = authenticated_client.get(reverse('profile-settings'))
        assert response.status_code == 200

    def test_user_can_change_username(self, authenticated_client, user):
        """Test that a user can change their username"""
        response = authenticated_client.post(reverse('profile-usernamechange'), {
            'username': 'newusername'
        })
        assert response.status_code == 302

        user.refresh_from_db()
        assert user.username == 'newusername'

    def test_unauthenticated_user_redirected_to_login(self, client):
        """Test that unauthenticated users are redirected to login"""
        response = client.get(reverse('profile-edit'))
        assert response.status_code == 302
        assert 'login' in response.url

    def test_profile_created_automatically_on_signup(self, db):
        """Test that a profile is created automatically when user signs up"""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='pass123'
        )
        assert hasattr(new_user, 'profile')
        assert new_user.profile is not None
