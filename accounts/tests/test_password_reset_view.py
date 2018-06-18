from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import mail
from django.core.urlresolvers import resolve
from django.urls import reverse
from django.test import TestCase


class PasswordResetTests(TestCase):

	def setUp(self):
		url = reverse('password_reset')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve(reverse('password_reset'))
		self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddleware')

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 2)
		self.assertContains(self.response, 'type="email', 1)


class SuccessfulPasswordResetTests(TestCase):

	def setUp(self):
		email = 'john@doe.com'
		User.objects.create_user(username='john', email=email, password='testtesttest')
		url = reverse('password_reset')
		self.response = self.client.post(url, {'email': email})

	def test_redireciton(self):
		url = reverse('password_reset_done')
		self.assertRedirects(self.response, url)

	def test_send_password_reset_email(self):
		self.assertEquals(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):

	def setUp(self):
		url = reverse('password_reset')
		self.response = self.client.post(url, {'email': 'donotexist@email.com'})

	def test_redirection(self):
		url = reverse('password_reset_done')
		self.assertRedirects(self.response, url)

	def test_no_reset_email_sent(self):
		self.assertEquals(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
	
	def setUp(self):
		url = reverse('password_reset_done')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve(reverse('password_reset_done'))
		self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetCofirmTests(TestCase):
	
	def setUp(self):
		user = User.objects.create_user(username='john', email='john@doe.com', password='testtesttest')

		self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
		self.token = default_token_generator.make_token(user)

		url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
		self.response = self.client.get(url, follow=True)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/reset/{}/{}/'.format(self.uid, self.token))
		self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, SetPasswordForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 3)
		self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):

	def setUp(self):
		user = User.objects.create_user(username='john', email='john@doe.com', password='testtesttest')
		
		self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
		self.token = default_token_generator.make_token(user)

		user.set_password('changedpassword')
		user.save()

		url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
		self.response = self.client.get(url, follow=True)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_html(self):
		password_reset_url = reverse('password_reset')
		self.assertContains(self.response, 'invalid password reset link')
		self.assertContains(self.response, 'href="{}"'.format(password_reset_url))


class PasswordResetCompleteTests(TestCase):

	def setUp(self):
		url = reverse('password_reset_complete')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve(reverse('password_reset_complete'))
		self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)