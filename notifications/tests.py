from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import Search, Websites
from .forms import SearchForm, RemoveForm

from account.models import User

class SearchModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@testing.com', password='12345', limit=10)
        self.website = Websites.objects.create(url="https://www.google.com", name="Google")
        self.search = Search.objects.create(terms_en="Test search", user=self.user)
        self.search.websites.add(self.website)

    def test_search_terms_max_length(self):
        search = Search.objects.get(pk=1)
        max_length = search._meta.get_field('terms_en').max_length
        self.assertEqual(max_length, 50)

    def test_search_str(self):
        search = Search.objects.get(pk=1)
        expected = search.terms_en
        self.assertEqual(expected, str(search))

class WebsitesModelTests(TestCase):
    def setUp(self):
        self.website = Websites.objects.create(url="https://www.google.com", name="Google")
    
    def test_websites_name_max_length(self):
        website = Websites.objects.get(pk=1)
        max_length = website._meta.get_field('name').max_length
        self.assertEqual(max_length, 25)

    def test_websites_str(self):
        website = Websites.objects.get(pk=1)
        expected = website.name
        self.assertEqual(expected, str(website))

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

    def test_search_form_terms_max(self):
        form = SearchForm()
        max_length = form.fields['terms_en'].max_length
        self.assertEqual(max_length, 50)

    def test_search_form_terms_min(self):
        form = SearchForm()
        max_length = form.fields['terms_en'].min_length
        self.assertEqual(max_length, 5)

class IndexViewTest(TestCase):
    def setUp(cls):
        limit = 10
        user = User.objects.create_user(username='test', email='test@testing.com', password='12345', limit=limit)
        website = Websites.objects.create(url="https://www.google.com", name="Google")

        for sid in range(limit):
            search = Search.objects.create(terms_en=f"test{sid}", user=user)
            search.websites.add(website)

    def test_view_url_exists(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_reverse(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/index.html')