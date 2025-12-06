from locust import HttpUser, task, between
import random
import string


class UserProfileUser(HttpUser):
    """
    Simulates real users interacting with the profile app
    """
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks

    def on_start(self):
        """
        Called when a simulated user starts - handles login
        """
        # Create a unique username for this test user
        self.username = f"testuser_{random.randint(1000, 9999)}"
        self.email = f"{self.username}@example.com"
        self.password = "testpass123"

        # Register/Login the user
        self.signup()
        self.login()

    def signup(self):
        """Create a new user account"""
        # Get the signup page first to get CSRF token
        response = self.client.get("/accounts/signup/")

        if response.status_code == 200:
            # Extract CSRF token from cookies
            csrftoken = response.cookies.get('csrftoken')

            # Submit signup form
            self.client.post(
                "/accounts/signup/",
                {
                    "username": self.username,
                    "email": self.email,
                    "password1": self.password,
                    "password2": self.password,
                },
                headers={"X-CSRFToken": csrftoken},
                catch_response=True
            )

    def login(self):
        """Login the user"""
        response = self.client.get("/accounts/login/")

        if response.status_code == 200:
            csrftoken = response.cookies.get('csrftoken')

            self.client.post(
                "/accounts/login/",
                {
                    "login": self.username,
                    "password": self.password,
                },
                headers={"X-CSRFToken": csrftoken}
            )

    @task(3)
    def view_own_profile(self):
        """View own profile - most common action"""
        self.client.get("/profile/", name="View Own Profile")

    @task(2)
    def view_profile_settings(self):
        """View profile settings page"""
        self.client.get("/profile/settings/", name="View Settings")

    @task(1)
    def edit_profile(self):
        """Edit profile information"""
        # Get edit page first
        response = self.client.get("/profile/edit/")

        if response.status_code == 200:
            csrftoken = response.cookies.get('csrftoken')

            # Generate random profile data
            random_name = ''.join(random.choices(string.ascii_letters, k=10))
            random_bio = f"This is a test bio {random.randint(1, 1000)}"

            # Submit edit form
            self.client.post(
                "/profile/edit/",
                {
                    "displayname": random_name,
                    "info": random_bio,
                },
                headers={"X-CSRFToken": csrftoken},
                name="Edit Profile"
            )

    @task(1)
    def change_username(self):
        """Change username"""
        response = self.client.get("/profile/settings/")

        if response.status_code == 200:
            csrftoken = response.cookies.get('csrftoken')

            # Generate new username
            new_username = f"user_{random.randint(10000, 99999)}"

            self.client.post(
                "/profile/usernamechange/",
                {"username": new_username},
                headers={"X-CSRFToken": csrftoken},
                name="Change Username"
            )

            # Update stored username
            self.username = new_username

    @task(1)
    def view_other_profile(self):
        """View another user's profile"""
        # Generate a random username to view
        random_user = f"testuser_{random.randint(1000, 9999)}"
        self.client.get(
            f"/profile/{random_user}/",
            name="View Other Profile",
            catch_response=True
        )


class AnonymousUser(HttpUser):
    """
    Simulates anonymous/unauthenticated users browsing profiles
    """
    wait_time = between(2, 5)

    @task(5)
    def view_random_profile(self):
        """Anonymous user trying to view profiles"""
        random_user = f"testuser_{random.randint(1000, 9999)}"
        self.client.get(
            f"/profile/{random_user}/",
            name="Anonymous - View Profile",
            catch_response=True
        )

    @task(1)
    def try_access_edit(self):
        """Anonymous user trying to access edit page (should redirect)"""
        self.client.get(
            "/profile/edit/",
            name="Anonymous - Try Edit",
            catch_response=True
        )

    @task(1)
    def try_access_settings(self):
        """Anonymous user trying to access settings (should redirect)"""
        self.client.get(
            "/profile/settings/",
            name="Anonymous - Try Settings",
            catch_response=True
        )
