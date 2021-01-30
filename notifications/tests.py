from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .models import Search, Websites
from .forms import SearchForm, RemoveForm

from account.models import User

# Creates a user with the given limit, and a number of search objects equal to the current limit minus the offset
def set_up_one_user(self, limit, offset):
    self.user = User.objects.create_user(username='test', email='test@testing.com', password='2HJ1vRV0Z&3iD', limit=limit)
    self.website = Websites.objects.create(url="https://www.google.com", name="Google")

    for sid in range(limit - offset):
        search = Search.objects.create(terms_en=f"test{sid}", user=self.user)
        search.websites.add(self.website)

class SearchModelTests(TestCase):
    # creates a user with a single search
    def setUp(self):
        user = User.objects.create_user(username='test', email='test@testing.com', password='2HJ1vRV0Z&3iD', limit=10)
        Search.objects.create(terms_en="test", user=user)
        self.search = Search.objects.get(terms_en="test")

    def test_search_terms_max_length(self):
        """
        A search object has a 'terms_en' field with max length of 50.
        """
        max_length = self.search._meta.get_field('terms_en').max_length
        self.assertEqual(max_length, 50)

    def test_search_str(self):
        """
        The string representation of a search object is given by the 'terms_en' value.
        """
        expected = self.search.terms_en
        self.assertEqual(expected, str(self.search))

    def test_search_details(self):
        """
        A search object has a details ArrayField with a max length of 150 for a single element in the field, and can be made null and blank.
        """
        details = self.search._meta.get_field('details')
        self.assertEqual(details.base_field.max_length, 150)
        self.assertEqual(details.null, True)
        self.assertEqual(details.blank, True)

class WebsitesModelTests(TestCase):
    # creates a single website in the database
    def setUp(self):
        self.website = Websites.objects.create(url="https://www.google.com", name="Google")
    
    def test_websites_name_max_length(self):
        """
        A website object has a 'name' field with a max_length of 25
        """
        max_length = self.website._meta.get_field('name').max_length
        self.assertEqual(max_length, 25)

    def test_websites_str(self):
        """
        The string representation of a website object is given by the 'name' value.
        """
        expected = self.website.name
        self.assertEqual(expected, str(self.website))

    def test_websites_url_right(self):
        """
        A website object has a 'url_right' field with a max_length of 100, and can be made null and blank.
        """
        field = self.website._meta.get_field('url_right')
        self.assertEqual(field.max_length, 100)
        self.assertEqual(field.null, True)
        self.assertEqual(field.blank, True)

class RemoveFormTests(TestCase):
    def test_remove_form_negative_pk(self):
        """
        A form with a negative value is not valid.
        """
        form = RemoveForm({'pk': -1})
        self.assertFalse(form.is_valid())

class SearchFormTests(TestCase):
    def test_search_form_label(self):
        """
        A search form has a 'terms_en' field with the label: 'Search terms.' 
        """
        form = SearchForm()
        self.assertEqual(form.fields['terms_en'].label, "Search terms")

    def test_search_form_terms_max(self):
        """
        A search form has a 'terms_en' field with a max length of 50 and a min length of 1.
        """
        form = SearchForm()
        max_length = form.fields['terms_en'].max_length
        min_length = form.fields['terms_en'].min_length
        self.assertEqual(max_length, 50)
        self.assertEqual(min_length, 1)

class IndexViewTest(TestCase):
    def test_view_url_exists(self):
        """
        Testing that the index page exists and the proper template is used.
        """
        response = self.client.get('')
        response2 = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'notifications/index.html')        

    def test_can_not_add_more(self):
        """
        A user is blocked on the index page from adding more test cases if they are at the limit.
        """
        set_up_one_user(self, 10, 0)
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<button id="modalButton" type="button" class="btn btn-info" data-toggle="modal" data-target="#myModal" disabled="True">Add new notification</button>')

    def test_view_displays_all(self):
        """
        All of a user's notifications should be displayed back at the index page.
        """
        set_up_one_user(self, 10, 0)
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test')
        self.assertEqual(len(response.context['data']), 10)

    def test_view_new_user(self):
        """
        A user that has not logged in should not have any notifications, and should see an introduction message if they visit the index page.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['data']), 0)
        self.assertContains(response, '<h2>Hello there</h2>')

class IndexPostTest(TestCase):
    def test_remove_form(self):
        """
        A user can submit a remove form to remove one of their notifications.
        """
        set_up_one_user(self, 10, 0)
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        s1 = Search.objects.get(terms_en="test1")
        self.assertEqual(s1.user, self.user)
        response = self.client.post(reverse('index'), {'pk': s1.pk})
        s2 = Search.objects.filter(terms_en="test1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(s2), 0)

    def test_remove_form_wrong_user(self):
        """
        A user cannot submit a remove form to remove a search object that belongs to another user.
        """
        set_up_one_user(self, 10, 0)
        user2 = User.objects.create(username='test2', email='test2@testing.com', password='2HJ1vRV0Z&3iD', limit=10)
        search = Search.objects.create(terms_en="test search", user=user2)
        search.websites.add(self.website)

        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        s1 = Search.objects.get(terms_en="test search")
        self.assertNotEqual(s1.user, self.user)
        response = self.client.post(reverse('index'), {'pk': search.pk})
        s2 = Search.objects.filter(terms_en="test search")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(s2), 1)

    def test_search_form(self):
        """
        A user can submit a search form to add a new notification to the database.
        """
        set_up_one_user(self, 10, 1)
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        website = Websites.objects.get(name="Google")
        response = self.client.post(reverse('index'), {'terms_en': 'Test Search', 'websites': [website.pk]})
        s = Search.objects.filter(terms_en="Test Search")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(s), 1)

    def test_search_form_limit(self):
        """
        A user cannot submit a search form to add a new notification to the database if they are currently at their limit.
        """
        set_up_one_user(self, 10, 0)
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('index'), {'terms_en': 'Test Search', 'websites': [0]})
        s = Search.objects.filter(terms_en="Test Search")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(s), 0)

# TODO: test ajax add/remove, getDetails

class DetailsViewTest(TestCase):
    def setUp(self):
        set_up_one_user(self, 10, 0)
        self.s = Search.objects.get(terms_en="test1")

    def test_view_url_exists(self):
        """
        Testing that the index page exists and the proper template is used.
        """
        response = self.client.get('/details/' + str(self.s.id))
        response2 = self.client.get(reverse('details', args=(self.s.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'notifications/details.html')
    
    def test_view_with_search(self):
        """
        A user will be displayed details associated with one of their search objects.
        """
        login = self.client.login(username='test', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('details', args=(self.s.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search'], self.s)

    def test_view_bad_search(self):
        """
        A user will be displayed an error if the details page they are trying to view is associated with a search belonging to another user or if it does not exist.
        """
        response = self.client.get(reverse('details', args=(self.s.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['search']), 0)