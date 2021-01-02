from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Search, Websites
from .forms import SearchForm, RemoveForm

class NewUserViews(TestCase):
    def test_new_user_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You currently don't have any notifications.")

    def test_new_user_add(self):
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please log in before adding a notification!")

class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@testing.com', password='12345')

    def test_add_search_user_id(self):
        s = Search.objects.create(terms_en="This is a test search", user_id=self.user.id)
        s2 = Search.objects.get(pk=1)
        self.assertEqual(1, s2.user_id)

class RemoveFormTests(TestCase):
    def test_remove_form_valid(self):
        form = RemoveForm({'pk': 1})
        self.assertTrue(form.is_valid())

    def test_remove_form_negative_pk(self):
        form = RemoveForm({'pk': -1})
        self.assertFalse(form.is_valid())

class SearchFormTests(TestCase):
    def test_search_form_label(self):
        form = SearchForm()
        self.assertEqual(form.fields['terms_en'].label, "Search terms")

    def test_search_form_all_fields(self):
        form = SearchForm({'terms_en': 'test'})
        self.assertFalse(form.is_valid())
