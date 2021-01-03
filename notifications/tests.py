from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .models import Search, Websites
from .forms import SearchForm, RemoveForm

from account.models import User

class SearchModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@testing.com', password='2HJ1vRV0Z&3iD', limit=10, at_limit=False)
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
    def setUp(self):
        limit = 10
        user = User.objects.create_user(username='test', email='test@testing.com', password='2HJ1vRV0Z&3iD', limit=limit, at_limit=True)
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

    def test_can_not_add_more(self):
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input class="btn btn-primary" type="button" value="Add a new notification" disabled>')

    def test_view_displays_all(self):
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test')
        self.assertEqual(len(response.context['data']), 10)

    def test_view_new_user(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['data']), 0)
        self.assertContains(response, '<h2>Hello there</h2>')

class NewViewTest(TestCase):
    def setUp(self):
        limit = 10
        user = User.objects.create_user(username='test', email='test@testing.com', password='2HJ1vRV0Z&3iD', limit=limit, at_limit=True)
        user2 = User.objects.create_user(username='test2', email='test2@testing.com', password='2HJ1vRV0Z&3iD', limit=limit, at_limit=False)
        website = Websites.objects.create(url="https://www.google.com", name="Google")

        for sid in range(limit-1):
            search = Search.objects.create(terms_en=f"test{sid}", user=user)
            search = Search.objects.create(terms_en=f"test{sid}", user=user2)
            search.websites.add(website)
        
        search = Search.objects.create(terms_en=f"test{limit}", user=user)
        search.websites.add(website)
    
    def test_view_url_exists(self):
        response = self.client.get('/new')
        self.assertEqual(response.status_code, 200)

    def test_view_reverse(self):
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/new.html')

    def test_view_new_user(self):
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Please log in before adding a notification!</h2>')
        self.assertNotContains(response, response.context['form'])

    def test_view_existing_user(self):
        login = self.client.login(username='test2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, response.context['form'])

    def test_view_existing_user_at_limit(self):
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, response.context['form'])
        self.assertContains(response, '<h2>You are at your limit. Please remove some notifications before adding new ones.</h2>')
