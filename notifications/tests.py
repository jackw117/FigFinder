from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Search
from .forms import SearchForm

class SearchAddTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test', email='test@testing.com', password='12345')
