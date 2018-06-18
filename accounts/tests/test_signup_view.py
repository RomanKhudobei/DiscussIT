from django.test import TestCase
from django.urls import resolve
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ..views import signup
from ..forms import SignUpForm


class SignUpTests(TestCase):

	def setUp(self):
		url = reverse('signup')
		self.response = self.client.get(url)

	def test_signup_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_signup_url_resolves_signup_view(self):
		view = resolve(reverse('signup'))
		self.assertEquals(view.func, signup)

	def test_signup_contains_csrf_token(self):
		self.assertContains(self.response, 'csrfmiddleware')

	def test_signup_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, SignUpForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input ', 5)
		self.assertContains(self.response, 'type="text"', 1)
		self.assertContains(self.response, 'type="email"', 1)
		self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):

	def setUp(self):
		url = reverse('signup')
		data = {
			'username': 'john',
			'email': 'john@doe.com',
			'password1': 'testtesttest',
			'password2': 'testtesttest'
		}
		self.response = self.client.post(url, data)
		self.home_url = reverse('home')

	def test_redirection(self):
		self.assertRedirects(self.response, self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authentication(self):
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):

	def setUp(self):
		url = reverse('signup')
		self.response = self.client.post(url, {})

	def test_signup_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_user_not_created(self):
		self.assertFalse(User.objects.exists())