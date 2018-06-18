from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board, Post, Topic
from ..views import reply_topic
from ..forms import NewPostForm


class ReplyTopicTestCase(TestCase):

	def setUp(self):
		self.board = Board.objects.create(name='Django', description='Django board')
		self.username = 'john'
		self.password = '123456'
		user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
		self.topic = Topic.objects.create(name='Hello, world!', board=self.board, starter=user)
		Post.objects.create(message='Test message goes here.', topic=self.topic, created_by=user)
		self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):

	def test_redirection(self):
		login_url = reverse('login')
		response = self.client.get(self.url)
		self.assertRedirects(response, f'{login_url}?next={self.url}')


class ReplyTopicTests(ReplyTopicTestCase):

	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.get(self.url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve(self.url)
		self.assertEquals(view.func, reply_topic)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddleware')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, NewPostForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 1)
		self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):

	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.post(self.url, {'message': 'test message'})

	def test_redirection(self):
		topic_posts_url = reverse('topic_posts', kwargs={'pk': 1, 'topic_pk': 1})
		self.assertRedirects(self.response, topic_posts_url)

	def test_reply_created(self):
		self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):

	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.post(self.url, {})

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)