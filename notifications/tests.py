from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Search
from .forms import SearchForm, RemoveForm

class NotificationViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test', email='test@testing.com', password='12345')

    def test_new_user_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You currently don't have any notifications.")

    # def test_one_notification_view(self):
    #     response = self.client.get(reverse('index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertQuerysetEqual(response.context, ["This is a test search"])

class SearchTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@testing.com', password='12345')

    def test_add_search_user_id(self):
        s = Search.objects.create(terms="This is a test search", user_id=self.user.id)
        s2 = Search.objects.get(pk=1)
        self.assertEqual(1, s2.user_id)

class RemoveFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@testing.com', password='12345')

    def test_remove_form_valid(self):
        s = Search.objects.create(terms="Test search", user_id=1)
        form = RemoveForm(data={'pk': 1})
        self.assertTrue(form.is_valid())

    def test_remove_form_negative_pk(self):
        form = RemoveForm(data={'pk': -1})
        self.assertFalse(form.is_valid())

class SearchFormTests(TestCase):
    def test_search_form_label(self):
        form = SearchForm()
        self.assertEqual(form.fields['terms'].label, "Search terms")

    def test_search_form_too_small(self):
        form = SearchForm({'terms': ''})
        self.assertFalse(form.is_valid())

    def test_search_form_too_large(self):
        form = SearchForm({'terms': 'Three Rings for the Elven-kings under the sky, Seven for the Dwarf-lords in their halls of stone, Nine for Mortal Men doomed to die, One for the Dark Lord on his dark throne'})
        self.assertFalse(form.is_valid())
