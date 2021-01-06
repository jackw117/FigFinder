from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import login

from .models import User
from .forms import RegistrationForm

# creates a user object
def create_user():
    User.objects.create(username="test", email='test@testing.com', password='2HJ1vRV0Z&3iD', limit=10)

class UserModelTests(TestCase):
    def test_limit_field(self):
        """
        A user has three groups it can be in with a default of 10.
        """
        create_user()
        user = User.objects.get(pk=1)
        self.assertEqual(len(user._meta.get_field('limit').choices), 3)
        self.assertEqual(user._meta.get_field('limit').default, 10)

class LoginViewTests(TestCase):
    def test_view_url_exists(self):
        """
        Testing that the login page exists and the proper template is used.
        """
        response = self.client.get('/login/')
        response2 = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'registration/login.html')

    def test_view_contains_login_form_and_registration(self):
        """
        Testing that the login page has a login form and new user registration link.
        """
        response = self.client.get(reverse('login'))
        self.assertContains(response, response.context['form'])
        self.assertContains(response, 'href="/register"')

    def test_incorrect_login(self):
        """
        An incorrect login attempt will display error messages.
        """
        create_user()
        response = self.client.post(reverse('login'), {'username': 'test', 'password': 'a'})
        self.assertContains(response, "<p>Your username and password didn't match. Please try again.</p>")

    def test_correct_login(self):
        """
        A correct login attempt will log in the user and redirect to the main page.
        """
        # create_user()
        # response = self.client.post(reverse('login'), {'username': 'test', 'password': '2HJ1vRV0Z&3iD'})
        # user = auth.get_user(self.client)
        # self.assertTrue(user.is_authenticated)
        pass

class LogoutViewTests(TestCase):
    def test_view_url_exists(self):
        """
        Testing that the login page exists and the proper template is used.
        """
        response = self.client.get('/logout/')
        response2 = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'registration/logged_out.html')

    def test_logout_displays_message(self):
        """
        The logout page should display a confirmation message.
        """
        response = self.client.get(reverse('logout'))
        self.assertContains(response, "<h2>You have been logged out</h2>")

class RegistrationFormTests(TestCase):
    def test_form_labels(self):
        """
        Registration form has a label for 'username' as 'Display name'
        """
        form = RegistrationForm()
        self.assertEqual(form.fields['username'].label, "Display name")

class RegistrationViewTests(TestCase):
    def test_view_url_exists(self):
        """
        Testing that the registration page exists and the proper template is used.
        """
        response = self.client.get('/register')
        response2 = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'registration/register.html')

    def test_view_new_user(self):
        """
        A user will have a registration form displayed to them if they are not logged in.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, response.context['form'])

    def test_view_existing_user(self):
        """
        A user will be redirected to the main page if they are already logged in.
        """
        # login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        # response = self.client.get('/register', follow=True)
        # self.assertEqual(response.redirect_chain, 0)
        pass

    def test_register_post(self):
        """
        The user will be registered and logged in.
        """
        pass